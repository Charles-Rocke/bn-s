from django.shortcuts import render
from rest_framework.generics import ListAPIView
from users.models import User
from .serializers import UserSerializer
# bn-s
from rest_framework.decorators import api_view
from rest_framework.response import Response
# bn-s
from django.http import HttpResponse, JsonResponse
import base64
import json
import uuid

from webauthn import (
    base64url_to_bytes,
    generate_authentication_options,
    generate_registration_options,
    options_to_json,
    verify_authentication_response,
    verify_registration_response,
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier
from webauthn.helpers.structs import (
    AttestationConveyancePreference,
    AuthenticationCredential,
    PublicKeyCredentialDescriptor,
    RegistrationCredential,
    UserVerificationRequirement,
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    RegistrationCredential,
    AuthenticationCredential,
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier
from users.models import Credential, UserAccount
from typing import Dict

RP_ID = 'bn-s.charles-rocke.repl.co'
RP_NAME = 'charles-rocke'
username = "johndoe@doe.com"

# Create your views here.
class RegisterAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view()
def handler_generate_registration_options(request):
    user_id = str(uuid.uuid4())
    print("got user id")
    # A simple way to persist credentials by user ID
    in_memory_db: Dict[str, UserAccount] = {}
    # Register our sample user
    in_memory_db[user_id] = UserAccount(
        id=user_id,
        username = username,
        credentials=[],
    )
    print(f"IN_MEMORY_DB type: {in_memory_db[user_id].username}")

    # Passwordless assumes you're able to identify the user before performing registration or
    # authentication
    logged_in_user_id = user_id
    user = in_memory_db[logged_in_user_id]
    
    options = generate_registration_options(
        rp_id=RP_ID,
        rp_name=RP_NAME,
        user_id=user.id,
        user_name=user.username,
        exclude_credentials=[{
            "id": cred.id,
            "transports": cred.transports,
            "type": "public-key"
        } for cred in user.credentials],
        authenticator_selection=AuthenticatorSelectionCriteria(
            user_verification=UserVerificationRequirement.REQUIRED),
        supported_pub_key_algs=[
            COSEAlgorithmIdentifier.ECDSA_SHA_256,
            COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
        ],
    )
    print("error free")
    current_registration_challenge = options.challenge
    print("OPTIONS TO JSON: ", options_to_json(options))
    opts = options_to_json(options)
    print("TYPE OPTS: ", type(opts))
    #convert string to  object
    json_opts = json.loads(opts)
    print(json_opts)
    return Response(json_opts)