from django.urls import path

from account.views import (ActivateUser, UserLoginView, UserLogoutView, \
                           UserRegistrationView, PasswordResetView, profile)

app_name: str = "account"

urlpatterns = [
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/<int:profile_id>/", profile, name="profile"),
    path("activate/<str:uuid64>/<str:token>/", ActivateUser.as_view(), name="activate_user"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
]
