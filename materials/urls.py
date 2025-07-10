from django.urls import path
from .views import (
    CourseViewSet,
    LessonListAPIView,
    LessonCreateAPIView,
    LessonUpdateAPIView,
    LessonRetrieveAPIView,
    LessonDestroyAPIView,
    CourseSubscribeAPIView,
)

from rest_framework.routers import DefaultRouter

# Описание маршрутизации для ViewSet
app_name = "materials"

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrive"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path(
        "lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "courses/<int:pk>/subscribe/",
        CourseSubscribeAPIView.as_view(),
        name="course_subscribe",
    ),
] + router.urls
