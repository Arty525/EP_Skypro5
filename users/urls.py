from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet
from rest_framework.routers import DefaultRouter

# Описание маршрутизации для ViewSet

app_name = "users"
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
urlpatterns = [
    path("list/", include(router.urls)),
    path("payment/", include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls