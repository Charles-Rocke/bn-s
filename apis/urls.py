from django.urls import path
import apis.views

# url patterns here
urlpatterns = [
	path("verify-authentication/", apis.views.hander_verify_authentication_response, name = "verify_auth_options"),
	path("generate-authentication-options/", apis.views.handler_generate_authentication_options, name = "generate_auth_options"),
	path("verify-registration-response/", apis.views.handler_verify_registration_response, name = "verify_options"),
    path("generate-registration-options/", apis.views.handler_generate_registration_options, name = "generate_options"),
	path("registration/username", apis.views.receiver_registration_username, name = "registration_username"),
]


