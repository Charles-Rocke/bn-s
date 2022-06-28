from django.urls import path
from .views import UserListView

# url patterns here
urlpatterns = [
    path("", UserListView.as_view(), name = "user_list")
]
