from django_user.forms import UserCreateForm, UserLoginForm
from django.views.generic.edit import CreateView, FormView


class SignupView(CreateView):
    form_class = UserCreateForm
    success_url = "/accounts/auth/login"
    template_name = "accounts/signup.html"

class LoginView(FormView):
	form_class = UserLoginForm
	success_url = "/portal/home"
	template_name = "registration/login.html"