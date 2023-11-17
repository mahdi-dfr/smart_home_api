from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'mobile_number', 'birth_date']

    def validate_mobile_number(self, value):
        if User.objects.filter(mobile_number=value).exists():
            raise ValidationError('این شماره قبلا در سیستم ثبت شده است!')
        return value

    # def validate_national_id(self, value):
    #     if User.objects.filter(national_id=value).exists():
    #         raise ValidationError('این کد ملی قبلا در سیستم ثبت شده است!')
    #     if not national_id_validator(value):
    #         raise ValidationError('کد ملی وارد شده معتبر نمیباشد!')
    #
    #     return value

    def validate_password(self, value):
        return make_password(value)
