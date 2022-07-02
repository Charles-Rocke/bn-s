from django.urls import path
from .views import HomePageView, UserView

# url patterns here
urlpatterns = [
    path("", HomePageView.as_view(), name = "user_list"),
	path("users/", UserView.as_view(), name = "users"),
]
