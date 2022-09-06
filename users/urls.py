from django.urls import path
from .views import HomePageView, UserView, PortalHomeView

# url patterns here
urlpatterns = [
  path("", HomePageView.as_view(), name = "home"),
	path("auth/", UserView.as_view(), name = "auth"),
	path("portal/home", PortalHomeView.as_view(), name = "portal_home"),
]
