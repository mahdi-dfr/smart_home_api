from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'mobile_number', 'birth_date']

    def validate_password(self, value):
        return make_password(value)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'mobile_number', 'role', ]
        read_only_fields = ('username', 'role')
        depth = 1
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
