from django.urls import include, path

from .views import SignupView, LoginView
from .apps import DjangoUserConfig

app_name = DjangoUserConfig.name

urlpatterns = [
	path("signup/", SignupView.as_view(), name="signup"),
	path("login/", LoginView.as_view(), name="login"),
]
