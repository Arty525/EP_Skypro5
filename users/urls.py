from django.urls import path, include

from .views import UserViewSet
from rest_framework.routers import DefaultRouter

# Описание маршрутизации для ViewSet

app_name = "users"
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
urlpatterns = [
    path("api/", include(router.urls)),
] + router.urls
