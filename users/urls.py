from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (
    EmailVerificationView,
    UserLoginView,
    UserRegistrationView,
)

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path(
        "verify/<uuid:code>/",
        EmailVerificationView.as_view(),
        name="email_verification",
    ),
]
