from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    telegram_id = models.CharField(max_length=50,blank=True, null=True, verbose_name="telegram_id")
    avatar = models.ImageField(upload_to='users/',blank=True, null=True, verbose_name="аватар")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
