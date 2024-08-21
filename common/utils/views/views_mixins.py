from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class TitleMixin:
    # Переменная класса, которую можно использовать для простых
    # (не динамически формируемых) заголовков
    title = None

    # Если нужен не захардкоженный динамически формируемый заголовок,
    # во вьюхе переопределить метод get_title и вместо self.title
    # подставить необходимые данные
    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context


class UserAlreadyAuthenticated(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        return True

    def handle_no_permission(self):
        return redirect("index")
