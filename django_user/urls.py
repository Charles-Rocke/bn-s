from django.urls import include, path

from .views import SignupView
from .apps import DjangoUserConfig

app_name = DjangoUserConfig.name

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("auth/", include("django.contrib.auth.urls")),
]
