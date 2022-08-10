from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "django_user/signup.html"
