from django_user.forms import UserCreateForm
from django.views.generic.edit import CreateView


class SignupView(CreateView):
    form_class = UserCreateForm
    success_url = "/accounts/auth/login"
    template_name = "accounts/signup.html"