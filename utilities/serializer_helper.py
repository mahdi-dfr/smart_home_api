from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField
from rest_framework.relations import RelatedField


def build_filters(request_data: dict, user_filter: dict) -> dict:
    result = {}

    for key in user_filter:
        if request_data.get(user_filter[key], None):
            result[key] = request_data.get(user_filter[key])

    return result


class CustomFilterMixin(RelatedField):
    def __init__(self, filter_params=None, force_filter=False, **kwargs):

        self.filter_params = filter_params
        self.force_filter = force_filter

        super().__init__(**kwargs)

    def get_queryset(self):
        if self.read_only or not self.filter_params:
            return super().get_queryset()

        assert self.queryset is not None, 'The queryset must not be empty'

        request = self.context.get('request', None)
        if not request:
            return self.queryset

        usable_filter = build_filters(request.data, self.filter_params)
        if self.force_filter and len(usable_filter) != len(self.filter_params):
            raise ValidationError(f"This fields are required: [{','.join(self.filter_params.values())}]")

        return self.queryset.filter(**usable_filter)


class FilterAblePrimaryKeyRelatedField(CustomFilterMixin, serializers.PrimaryKeyRelatedField):
    pass


class CustomSlugRelatedField(CustomFilterMixin, serializers.SlugRelatedField):

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(id=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')


class NestedObjectRelatedField(serializers.RelatedField):
    def __init__(self, rep_serializer, input_field='id', **kwargs):
        assert rep_serializer is not None, 'The `rep_serializer` argument is required.'
        assert input_field is not None, 'The `input_field` argument is required.'
        self.rep_serializer = rep_serializer
        self.input_field = input_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(**{self.input_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.input_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, value):
        return self.rep_serializer(instance=value).data


class DisplayTextChoicesField(ChoiceField):

    def to_representation(self, value):
        return self.choices.get(super().to_representation(value))
