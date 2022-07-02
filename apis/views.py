from django.shortcuts import render
from rest_framework.generics import ListAPIView
from users.models import UserAccount, Credential
# bn-s
from rest_framework.decorators import api_view
from rest_framework.response import Response
# bn-s
from django.contrib.auth import get_user_model
from pprint import pprint
import base64
import json
import uuid
import requests

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
from users.models import Credential, UserAccount, User, UserCredential
from typing import Dict

RP_ID = 'bn-s.charles-rocke.repl.co'
RP_NAME = 'charles-rocke'
username = "johndoe@doe.com"
origin = "https://bn-s.charles-rocke.repl.co"
# A simple way to persist credentials by user ID
global in_memory_db
in_memory_db: Dict[str, UserAccount] = {}

# Create your views here
@api_view()
def handler_generate_registration_options(request):
	global current_registration_challenge
	global logged_in_user_id
	# create a unique user id
	user_id = str(uuid.uuid4())
    
    # Register new user
	in_memory_db[user_id] = UserAccount(
        id=user_id,
        username = username,
        credentials=[],
    )
    # Passwordless assumes you're able to identify the user before performing registration or authentication
	logged_in_user_id = user_id
	user = in_memory_db[logged_in_user_id]

	# get UserAccount id and username
	print(in_memory_db[user_id].username)

	
	# initialize new user
	new_user = User(id = in_memory_db[user_id].id, username = in_memory_db[user_id].username)
	Xser = get_user_model()
	users = Xser.objects.all()
	print("CURRENT USERS: ", users)
	# generate registration options
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
    
	current_registration_challenge = options.challenge
	opts = options_to_json(options)
    #convert string to  object
	json_opts = json.loads(opts)
	return Response(json_opts)

# add user to local database for later authentication

@api_view(['GET', 'POST'])
def handler_verify_registration_response(request):
	if request.method == "POST":
	    print(request.method)
	    global current_registration_challenge
	    global logged_in_user_id

		# get the request body
	    body = request.body
	    body_parsed = json.loads(body)
	    print("BODY_PARSED: ", body_parsed)
	    try:
	        credential = RegistrationCredential.parse_raw(body)
	        verification = verify_registration_response(
	            credential=credential,
	            expected_challenge=current_registration_challenge,
	            expected_rp_id=RP_ID,
	            expected_origin=origin,
	        )
	    except Exception as err:
	        return {"verified": False, "msg": str(err), "status": 400}
		
	    user = in_memory_db[logged_in_user_id]
	
	    new_credential = Credential(
	        id=verification.credential_id,
	        public_key=verification.credential_public_key,
	        sign_count=verification.sign_count,
	        transports=json.loads(body).get("transports", []),
	    )
	
	    user.credentials.append(new_credential)
	    print("appending new credential")

	    cred_opts = options_to_json(credential)
	    #convert string to  object
	    json_opts = json.loads(cred_opts)
	    return Response(json_opts)
	