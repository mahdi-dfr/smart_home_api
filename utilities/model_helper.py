from re import search

from django.core.exceptions import ValidationError
from django.db.models import QuerySet


class RoleBaseQuerySetMixin(QuerySet):
    def filter_by_role(self, **kwargs) -> QuerySet:
        raise NotImplementedError


def national_id_validator(value):
    if not search(r'^\d{10}$', value):
        raise ValidationError(f'{value} یک کد ملی معتبر نمیباشد! ')

    check = int(value[9])
    s = sum([int(value[x]) * (10 - x) for x in range(9)]) % 11
    if not ((2 > s == check) or (s >= 2 and check + s == 11)):
        raise ValidationError(f'{value} یک کد ملی معتبر نمیباشد! ')


def mobile_validator(value):
    if len(value) != 11:
        raise ValidationError('شماره موبایل باید 11 رقم باشد!')

    if not str(value).startswith('09'):
        raise ValidationError('شماره موبایل با 09 شروع شود!')

    if not str(value).isdigit():
        raise ValidationError('نمیتوان در شماره موبایل از حروف استفاده کرد!')


def tell_number_validator(value):
    if len(value) != 11:
        raise ValidationError('شماره تلفن باید 11 رقم باشد!')

    if not str(value).startswith('0'):
        raise ValidationError('شماره تلفن با پیش شماره شروع شود!')

    if not str(value).isdigit():
        raise ValidationError('نمیتوان در شماره تلفن از حروف استفاده کرد!')

