from django.urls import path
from .views import HomePageView, UserView

# url patterns here
urlpatterns = [
    path("", HomePageView.as_view(), name = "register"),
	path("auth/", UserView.as_view(), name = "auth"),
]
