# bn-s
from rest_framework.decorators import api_view
from rest_framework.response import Response
# bn-s

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
from users.models import Credential, UserAccount, Users, UserCredential
from typing import Dict
#####################################################

#####################################################
# Global variables
RP_ID = 'bn-s.charles-rocke.repl.co'
RP_NAME = 'charles-rocke'
username = "applengineer@handsome.com"
origin = "https://bn-s.charles-rocke.repl.co"
# A simple way to persist credentials by user ID
global in_memory_db
in_memory_db: Dict[str, UserAccount] = {}
# end global variable

# Create your views here
# generate sign up options
@api_view()
def handler_generate_registration_options(request):
	global current_registration_challenge
	global logged_in_user_id
	global new_user
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
	# print(in_memory_db[user_id].username)

	
	# initialize new user
	new_user = Users(id = in_memory_db[user_id].id, username = in_memory_db[user_id].username)
	# save new user 
	new_user.save()
	print("NEW_USER ID:", new_user.id)
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
	print(json_opts)
	return Response(json_opts)

# verify registration response
@api_view(['GET', 'POST'])
def handler_verify_registration_response(request):
	print(request.method)
	if request.method == "POST":
	    
	    print(request.method)
	    global current_registration_challenge
	    global logged_in_user_id

		# get the request body
	    body = request.body
	    
	    try:
	        credential = RegistrationCredential.parse_raw(body)
	        print("25%")
	        verification = verify_registration_response(
	            credential=credential,
	            expected_challenge=current_registration_challenge,
	            expected_rp_id=RP_ID,
	            expected_origin=origin,
	        )
	    except Exception as err:
	        return {"verified": False, "msg": str(err), "status": 400}
		
	    user = in_memory_db[logged_in_user_id]
	    print("50%")
	    new_credential = Credential(
	        id=verification.credential_id,
	        public_key=verification.credential_public_key,
	        sign_count=verification.sign_count,
	        transports=json.loads(body).get("transports", []),
	    )
	    print("NEW_CREDENTIAL.ID & .PUBLIC_KEY:", new_credential.id,"\n", new_credential.public_key)
#######################################################
#######################################################	
	    user.credentials.append(new_credential)
		# view users new credential
	    print("appending new credential")
#######################################################
	    # add credential to Users Credential Model
	    print("USER: ", user)
	    print("NEW_USER ID:", new_user.id)
	    print("ASSIGNNING NEW_CRED")
	    global new_cred
	    new_cred = UserCredential(id=new_credential.id, public_key=new_credential.public_key, sign_count=new_credential.sign_count, transports=json.loads(body).get("transports", []), user = new_user)
	    new_cred.save()
	    print("ASSIGNNING NEW_CRED COMPLETE")
	    print("NEW_CRED.PUBLIC_KEY: ", new_cred.public_key)
#######################################################
	    cred_opts = options_to_json(credential)
	    #convert string to  object
	    json_opts = json.loads(cred_opts)
	    
	    return Response(json_opts)

		
# generate authentication options
@api_view(['GET', 'POST'])
def handler_generate_authentication_options(requests):
	global current_authentication_challenge
	global logged_in_user_id
	
	# current user
	user = in_memory_db[logged_in_user_id]

	# generating authentication options
	options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=[{
            "type": "public-key",
            "id": cred.id,
            "transports": cred.transports
        } for cred in user.credentials],
        user_verification=UserVerificationRequirement.REQUIRED,
    )
	
	# getting current auth challenge
	current_authentication_challenge = options.challenge

	# converting authentication options to json
	opts = options_to_json(options)
	
    # convert authentication options string to  object
	json_opts = json.loads(opts)

	# return django rest framework response
	return Response(json_opts)

	
# verify authentication response
@api_view(['GET', "POST"])
def hander_verify_authentication_response(request):
	if request.method == "POST":
	    print("0%")
	    global current_registration_challenge
	    global logged_in_user_id

		# get the request body
	    body = request.body
	    print("10%")
	    try:
			# try to get auth credential body
		    credential = AuthenticationCredential.parse_raw(body)
			
	        # Find the user's corresponding public key #
			# current user is the user that is logged in
		    user = in_memory_db[logged_in_user_id]
		    
			# user credential set to None for now
		    user_credential = None

			# for each Credential object in a users credential list
		    for _cred in user.credentials:
				# if the users credential id matches auth credential id
			    if _cred.id == credential.raw_id:
					# user credential = the Credential object
				    user_credential = _cred

			# if user_credential is None raise an exception
		    if user_credential is None:
			    raise Exception("Could not find corresponding public key in DB")
		    print("50%")
		    print(UserCredential.public_key)
		    # print(type(new_user.public_key))
		    print(user_credential.public_key)
		    # print(type(user_credential.public_key))
	        # Verify the assertion
		    verification = verify_authentication_response(
	            credential=credential,
	            expected_challenge=current_authentication_challenge,
	            expected_rp_id=RP_ID,
	            expected_origin=origin,
	            credential_public_key=new_cred.public_key,
	            credential_current_sign_count=user_credential.sign_count,
	            require_user_verification=True,
	        )
	    except Exception as err:
		     return {"verified": False, "msg": str(err), "status": 400}

	    print("75%")
	    # Update our credential's sign count to what the authenticator says it is now
	    user_credential.sign_count = verification.new_sign_count

		# converting verification options to json
	    opts = options_to_json(verification)
		
	    # convert verification options string to  object
	    json_opts = json.loads(opts)
	    print("100%")
		# return django rest framework response
	    return Response(json_opts)