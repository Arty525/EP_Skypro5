from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="E-mail")

    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=50, verbose_name="Номер телефона")
    city = models.CharField(max_length=50, verbose_name="Город")
    avatar = models.ImageField(
        upload_to="avatars/", verbose_name="Аватар", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    EXCLUDE_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} - {self.email}"
