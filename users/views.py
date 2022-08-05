<<<<<<< HEAD
from django.views.generic import TemplateView, ListView, FormView, CreateView
from .models import User
from .forms import UserNameForm
=======
from django.contrib.auth import get_user_model
from django.views.generic import ListView, FormView
>>>>>>> 3f587ca449e474fea6db8d91ec9495290cbd8dc6
from django.urls import reverse_lazy

from .forms import UserNameForm

# Create your views here.
class HomePageView(CreateView):
	template_name = "users/register.html"
	success_url = reverse_lazy("auth")
	model = User
	fields = ['username']

class UserView(ListView):
	model = get_user_model()
	template_name = "users/auth.html"