from django.contrib.auth import get_user_model
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy

from .forms import UserNameForm

# Create your views here.
class HomePageView(FormView):
	form_class = UserNameForm
	template_name = "users/register.html"
	success_url = reverse_lazy("auth")

class UserView(ListView):
	model = get_user_model()
	template_name = "users/auth.html"