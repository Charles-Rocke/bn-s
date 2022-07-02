from django.urls import path
from .views import handler_generate_registration_options, handler_verify_registration_response

# url patterns here
urlpatterns = [
	path("verify-registration-response/", handler_verify_registration_response, name = "verify_options"),
    path("generate-registration-options/", handler_generate_registration_options, name = "generate_options"),
]


