from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView

from account.forms import UserLoginForm, UserRegistrationForm
from account.services.emails import send_registration_email
from account.services.mixins import TitleMixin
from core.utils.token_generator import TokenGenerator


class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    template_name: str = "registration/login.html"
    title: str = "Login"
    model = get_user_model()
    form_class = UserLoginForm
    success_message = "You are successfully logged in"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        remember_me = form.cleaned_data["remember_me"]
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    template_name: str = "registration/registration.html"
    title: str = "Registration"
    model = get_user_model()
    form_class = UserRegistrationForm
    success_url = reverse_lazy("account:login")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_registration_email(request=self.request, user_instance=self.object)
        return super().form_valid(form)


class ActivateUser(RedirectView):
    url = reverse_lazy("core:index")

    def get(self, request, uuid64, token, *args, **kwargs):

        try:
            pk = force_str(urlsafe_base64_decode(uuid64))
            current_user = get_user_model().objects.get(pk=pk)
        except (ValueError, get_user_model().DoesNotExist, TypeError):
            return HttpResponse("Activation link is invalid")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(request, current_user)

            return super().get(request, *args, **kwargs)

        return HttpResponse("Activation link is invalid")


class ResetPasswordView(TitleMixin, SuccessMessageMixin, PasswordResetView):
    template_name: str = "registration/password/password_reset.html"
    title: str = "Reset Password"
    success_url = reverse_lazy("account:login")
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    subject_template_name: str = "registration/password/password_reset_subject.html"
    email_template_name: str = "registration/password/password_reset_email.txt"
