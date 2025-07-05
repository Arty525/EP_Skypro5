from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateUserAPIView, UserListAPIView, UserRetrieveAPIView, UserDestroyAPIView, UserUpdateAPIView

app_name = "users"
urlpatterns = [
    path('list/', UserListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('delete/<int:pk>', UserDestroyAPIView.as_view(), name='delete_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', CreateUserAPIView.as_view(), name='registration'),
    path('update/<int:pk>', UserUpdateAPIView.as_view(), name='update_user'),

]