from django.urls import path
from .views import RegisterAPIView, handler_generate_registration_options

# url patterns here
urlpatterns = [
    path("", RegisterAPIView.as_view(), name = "register_api_view"),
    path("generate-registration-options/", handler_generate_registration_options, name = "generate_options"),
]


