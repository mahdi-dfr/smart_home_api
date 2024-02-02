import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from persiantools.jdatetime import JalaliDate
from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, DateField
from rest_framework.relations import RelatedField

from utilities.utility import jalali_to_gregorian, gregorian_to_jalali


def build_filters(request_data: dict, user_filter: dict) -> dict:
    result = {}

    for key in user_filter:
        if request_data.get(user_filter[key], None):
            result[key] = request_data.get(user_filter[key])

    return result


class CustomSlugRelatedField(SlugRelatedField):

    def __init__(self, filter_params=None, force_filter=False, use_on_select=True, is_many=False, slug_field=None,
                 **kwargs):

        self.filter_params = filter_params
        self.force_filter = force_filter
        self.use_on_select = use_on_select
        self.is_many = is_many

        super().__init__(slug_field, **kwargs)

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

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(id=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        if not self.use_on_select:
            return super().to_representation(obj)

        data = {
            'value': getattr(obj, 'id'),
            'text': super().to_representation(obj)
        }

        if self.is_many:
            return data

        return [data]


class NestedObjectRelatedField(RelatedField):
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
        if value in ('', None):
            return [{}]
        return [{
            'value': value,
            'text': self.choices.get(value)
        }]


class JalaliDateField(serializers.DateField):
    def to_representation(self, value):
        if value:
            jalali_date = JalaliDate(value.year, value.month, value.day)
            return f"{jalali_date.year}-{jalali_date.month:02d}-{jalali_date.day:02d}"
        return None

    def to_internal_value(self, value):
        try:
            jalali_date_parts = [int(part) for part in value.split('/')]
            georgian_date = JalaliDate(*jalali_date_parts).to_gregorian()
            return georgian_date
        except (ValueError, IndexError):
            raise serializers.ValidationError("فرمت تاریخ اشتباه است. از این فرمت استفاده کنید: 'YYYY/MM/DD'. ")

