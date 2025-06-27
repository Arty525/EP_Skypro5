from django.urls import path, include
from .views import (
    CourseViewSet,
    LessonList,
    LessonCreate,
    LessonUpdate,
    LessonRetrieve,
    LessonDestroy,
)

from rest_framework.routers import DefaultRouter

# Описание маршрутизации для ViewSet
app_name = "materials"

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonList.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieve.as_view(), name="lesson_retrive"),
    path("lessons/create/", LessonCreate.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/delete/", LessonDestroy.as_view(), name="lesson_delete"),
    path("lessons/<int:pk>/update/", LessonUpdate.as_view(), name="lesson_update"),
] + router.urls
