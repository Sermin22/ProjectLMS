from django.urls import path
from users.apps import UsersConfig
from users.views import (PaymentsListAPIView, CustomUserCreateAPIView, CustomUserListAPIView,
                         CustomUserRetrieveAPIView, CustomUserUpdateAPIView, CustomUserDestroyAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
    path("register/", CustomUserCreateAPIView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", CustomUserListAPIView.as_view(), name="users_list"),
    path("users/<int:pk>/", CustomUserRetrieveAPIView.as_view(), name="users_retrieve"),
    path("users/create/", CustomUserCreateAPIView.as_view(), name="users_create"),
    path("users/<int:pk>/update/", CustomUserUpdateAPIView.as_view(), name="users_update"),
    path("users/<int:pk>/delete/", CustomUserDestroyAPIView.as_view(), name="users_delete"),
]
