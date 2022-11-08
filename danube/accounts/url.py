from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LogoutAPIView,
    VerifyEmail,
    LoginAPIView,
    UserViewSet,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="api-register"),
    path("login/", LoginAPIView.as_view(), name="api-login"),
    path("logout/", LogoutAPIView.as_view(), name="api-logout"),
    path("email-verify/", VerifyEmail.as_view(), name="api-email-verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("<int:pk>/", UserViewSet.as_view({"get": "retrieve", "patch": "partial_update"}), name="users-details"),
]
