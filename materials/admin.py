from django.contrib import admin

from materials.models import Course, Lesson


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'owner'
    )
    list_filter = (
        'owner',
    )
    search_fields = ("title", "description")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'owner',
        'course'
    )
    list_filter = (
        'owner',
        'course',
    )
    search_fields = ("title", "description")