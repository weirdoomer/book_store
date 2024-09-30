from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from common.utils.views.views_mixins import (
    TitleMixin,
    UserAlreadyAuthenticated,
)
from users.forms import UserLoginForm, UserRegistrationForm
from users.models import EmailVerification, User
from users.tasks import send_email_verification


class UserLoginView(TitleMixin, UserAlreadyAuthenticated, LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    title = "Авторизация"


class UserRegistrationView(
    TitleMixin, UserAlreadyAuthenticated, SuccessMessageMixin, CreateView
):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")
    success_message = "Вы успешно зарегестрированы!"
    title = "Регистрация"

    def form_valid(self, form):
        user = form.save()
        send_email_verification.delay(user.id)
        return super().form_valid(form)


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Подтверждение электронной почты"
    template_name = "users/email_verification.html"

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        user = EmailVerification.objects.get(code=code).user
        email_verifications = EmailVerification.objects.filter(
            user=user, code=code
        )
        if (
            email_verifications.exists()
            and not email_verifications.first().is_expired()
        ):
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(
                request, *args, **kwargs
            )
        else:
            return HttpResponseRedirect(reverse("index"))


class ProfileView(LoginRequiredMixin, TitleMixin, DetailView):
    model = User
    title = "Профиль"
    template_name = "users/profile.html"

    def get_object(self):
        return self.request.user
