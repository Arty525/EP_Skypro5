from django.db import models

from users.models import User


# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="previews/courses/", verbose_name="Превью", blank=True, null=True
    )
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="previews/lessons/", verbose_name="Превью", blank=True, null=True
    )
    video_url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title", "course"]
