from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    # Для устранения ошибки при создании пользователя без username
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="E-mail")
    first_name = models.CharField(
        max_length=50, verbose_name="Имя", null=True, blank=True
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия", null=True, blank=True
    )
    phone_number = models.CharField(
        max_length=50, verbose_name="Номер телефона", null=True, blank=True
    )
    city = models.CharField(max_length=50, verbose_name="Город", null=True, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/", verbose_name="Аватар", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["id"]


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(
        "materials.Course", on_delete=models.CASCADE, null=True, blank=True
    )
    lesson = models.ForeignKey(
        "materials.Lesson", on_delete=models.CASCADE, null=True, blank=True
    )
    amount = models.IntegerField(default=0)
    payment_method = models.CharField()

    def __str__(self):
        return (f"{self.user} - {self.payment_date} - "
                f"{self.course} - {self.amount} - {self.payment_method} - {self.lesson}")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["payment_date"]
