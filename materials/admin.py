from django.contrib import admin

from materials.models import Course, Lesson, Subscriptions


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "owner", "last_updated")
    list_filter = ("owner", "last_updated")
    search_fields = ("title", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "owner", "course", "last_updated")
    list_filter = (
        "owner",
        "course",
        "last_updated",
    )
    search_fields = ("title", "description")


@admin.register(Subscriptions)
class SubsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course")
    list_filter = (
        "user",
        "course",
    )
    search_fields = ("user", "course")
