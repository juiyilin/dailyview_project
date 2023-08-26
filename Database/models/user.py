from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, verbose_name='帳號')
    password = models.CharField(max_length=128, verbose_name='密碼')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'User'


class LogoutToken(models.Model):
    token = models.CharField(max_length=256, verbose_name='登出token', db_index=True)
    logout_time = models.DateTimeField(auto_now_add=True, verbose_name='登出時間')

    class Meta:
        db_table = 'LogoutToken'
