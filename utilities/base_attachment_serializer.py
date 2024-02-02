from rest_framework import serializers
from collections import OrderedDict
from rest_framework.settings import api_settings
from rest_framework.exceptions import ValidationError as DRFValidationError, ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.fields import SkipField, get_error_detail, set_value
from collections.abc import Mapping


class BaseAttachmentSerializer(serializers.ModelSerializer):
    attachments_field_name = 'attachments'
    model_field_name = None
    attachment_model = None
    attachment_serializer = None

    def create(self, validated_data):
        attachments_list = self.context.get('view').request.FILES.getlist(self.attachments_field_name)
        instance = super().create(validated_data)
        for attach in attachments_list:
            self.attachment_model.objects.create(**{self.model_field_name: instance, 'attachments': attach})
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        attachments = self.context.get('view').request.FILES.getlist(self.attachments_field_name)
        self.attachment_model.objects.filter(**{self.attachments_field_name: instance}).delete()
        for attachment in attachments:
            self.attachment_model.objects.create(**{self.attachments_field_name: instance, 'attachments': attachment})
        return instance

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        """
        if not isinstance(data, Mapping):
            message = self.error_messages['invalid'].format(
                datatype=type(data).__name__
            )
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='invalid')

        ret = OrderedDict()
        errors = OrderedDict()
        fields = self._writable_fields

        attachments = self.context.get('view').request.FILES.getlist('attachments')
        if len(attachments) < 1:
            errors['attachments'] = ['This field is required.']

        for field in fields:
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            primitive_value = field.get_value(data)
            try:
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                errors[field.field_name] = exc.detail
            except DjangoValidationError as exc:
                errors[field.field_name] = get_error_detail(exc)
            except SkipField:
                pass
            else:
                set_value(ret, field.source_attrs, validated_value)

        if errors:
            raise ValidationError(errors)

        return ret

