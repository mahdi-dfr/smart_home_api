from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    class Meta:
        verbose_name = 'کاربران (همه)'
        verbose_name_plural = 'کاربران (همه)'

    ROLE = [
        ('0', 'نصاب'),
        ('1', 'کاربر عادی'),
    ]
    role = models.CharField(max_length=1, choices=ROLE, default='1')
    email = models.CharField(max_length=100, verbose_name='ایمیل', null=False)
    mobile_number = models.CharField(max_length=11, verbose_name='شماره موبایل', null=True)
    birth_date = models.CharField(max_length=10, verbose_name='تاریخ تولد', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    last_login = models.DateTimeField(auto_now=True, blank=True, verbose_name='آخرین ورود')
    create_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    delete_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')
    update_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ حذف')

    def __str__(self):
        return self.username
