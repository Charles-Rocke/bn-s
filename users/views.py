from django.views.generic import TemplateView, ListView, FormView
from .models import Users
from .forms import UserNameForm
from django.urls import reverse_lazy
# Create your views here.
class HomePageView(FormView):
	form_class = UserNameForm
	template_name = "users/register.html"
	success_url = reverse_lazy("auth")

class UserView(ListView):
	model = Users
	template_name = "users/auth.html"