import os
import sys
# bn-s
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# getting the name of registration username file

# getting correct user
from django.shortcuts import get_object_or_404


# bn-s
import json

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
from django_user.models import UserCredential

from django.http import HttpResponse
#####################################################
# for authenticating users
from django_user.models import User

from django.contrib.auth import get_user_model


#####################################################
# Global variables
RP_ID = 'bn-s.charles-rocke.repl.co'
RP_NAME = 'charles-rocke'
origin = "https://bn-s.charles-rocke.repl.co"
# A simple way to persist credentials by user ID

# delete below 
#__location__ = os.path.realpath(
#    os.path.join(os.getcwd(), os.path.dirname(__file__)))
# end delete

# Create your views here

# creating a file for input username to be stored
# if text/plain is a header value, dont run
@api_view(['GET', 'POST'])
@never_cache
def receiver_registration_signup(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		registration_username = json.load(request)['post_data']
		print(f"data: {registration_username}")

		# Open in "wb" mode to
		# write users registration name to a new file
		print("WRITING FILE")
		with open("/home/runner/bn-s/apis/signup_username_file.txt", "w") as username_file:
			# Write bytes to file
			username_file.write(registration_username)
		print("FINISHED WRITING FILE")

		# return the binary filename
		return Response(status=status.HTTP_200_OK)


# generate sign up options
@api_view(['GET', 'POST'])
@never_cache
def handler_generate_registration_options(request):
	
	# read users registered name from registration_username file
	print("opening")
	with open("/home/runner/bn-s/apis/signup_username_file.txt", "r") as username_file:
		username = username_file.read()
		print(f"username: {username}")
		if username:
			user = User.objects.create(username = username)
			user1 = get_object_or_404(User, username=username)
			print("user1:", user1)
	# generate registration options
	# user.id must be a string for encoding
	print("GENERATE REG OPTIONS")
	options = generate_registration_options(
		rp_id=RP_ID,
		rp_name=RP_NAME,
		user_id=str(user.id),
		user_name=user.username,
		exclude_credentials=[{
			"id": str(user.id),
			"transports": ["internal", "nfc", "usb"],
			"type": "public-key"
		} for cred in user.credentials],
		
		authenticator_selection=AuthenticatorSelectionCriteria(
			user_verification=UserVerificationRequirement.REQUIRED),
		supported_pub_key_algs=[
			COSEAlgorithmIdentifier.ECDSA_SHA_256,
			COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
		],
	)
	print("FINISHED GENERATING REG OPTIONS")
	current_registration_challenge = options.challenge
	# Open in "wb" mode to
	# write current_registration_challenge to a new file
	print("WRITING FILE")
	with open("registration_challenge.txt", "wb") as binary_file:
		# Write bytes to file
		binary_file.write(current_registration_challenge)
	print("FINISHED WRITING FILE")

	print("OPTIONS TO JSON")
	opts = options_to_json(options)
	print("FINISHED OPTIONS TO JSON")
	
	#convert string to  object
	print("JSON LOADS OPTIONS")
	print(type(json.dumps(opts)))
	json_opts = json.loads(opts)
	print(json_opts)
	print("FINISHED JSON LOADS")

	print("PRINTING JSON OPTIONS")
	print(HttpResponse(json_opts))
	print(type(HttpResponse(json_opts)))

	print("RETURNING JSON OPTIONS")
	return Response(json_opts)
#########################################################

# verify registration response
@api_view(['GET', 'POST'])
def handler_verify_registration_response(request):
	print()
	print("start of verify reg handler")
	if request.method == "POST":
		print("POST")
	    
		
		# get the request body
		body = request.body
		
	    
		try:
			credential = RegistrationCredential.parse_raw(body)
			# getting credenial challenge 
			with open("registration_challenge.txt", "rb") as challenge_file:
				challenge_file_content = challenge_file.read()
					
	
			# converting credential challenge to an encoded byte
			verification = verify_registration_response(
				credential=credential,
				expected_challenge=challenge_file_content,
				expected_rp_id=RP_ID,
				expected_origin=origin,
			)
		except Exception as err:
			print()
			print(f"ERROR: {err}")
			#return {"verified": False, "msg": str(err), "status": 400}
		
		print("50%")
	
		# creating users credential
		new_credential = UserCredential(
			id=verification.credential_id,
			public_key=verification.credential_public_key,
			sign_count=verification.sign_count,
			transports=json.loads(body).get("transports", []),
		)
	
		# after verification, user must be the currently logged in user
		# current user = verified registrant
		with open("/home/runner/bn-s/apis/signup_username_file.txt", "r") as username_file:
			username = username_file.read()
			print(username)

		# finding the user with the entered username
		print("user or 404")
		user = get_object_or_404(User, username=username)
		print("user: ", user)
		new_cred = UserCredential.objects.create(id=new_credential.id, public_key=new_credential.public_key, sign_count=new_credential.sign_count, transports=json.loads(body).get("transports", []), username = user)
		print("ASSIGNNING NEW_CRED COMPLETE")
		print("NEW_CRED.PUBLIC_KEY: ", new_cred.public_key)
		print("NEW_CRED.ID: ", new_cred.id)
		
		# assign new credential to user
		print(f"USER.CREDENTIALS1: {user.credentials}")
		user = User.objects.get(username= username)
		print(f"USER.CREDENTIALS2: {user.credentials}")
		# set credential attribute for user
		print(user.username)
		setattr(user, 'credentials', str(new_credential))
		user.save()
		cred_opts = options_to_json(credential)
		#convert string to  object
		json_opts = json.loads(cred_opts)

		registration_challenge_file = "registration_challenge.txt"
		username_file = "/home/runner/bn-s/apis/signup_username_file.txt"
		os.remove(registration_challenge_file)
		os.remove(username_file)
		print("data removed and user/user credential created")
		
	return Response(json_opts)

#########################################################
# end registration 


# start authentication
#########################################################

@api_view(['GET', 'POST'])
@never_cache
def receiver_registration_login(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		registration_username = json.load(request)['post_data']
		print(f"data: {registration_username}")

		# Open in "wb" mode to
		# write users registration name to a new file
		print("WRITING FILE")
		with open("/home/runner/bn-s/apis/login_username_file.txt", "w") as login_file:
			# Write bytes to file
			login_file.write(registration_username)
		print("FINISHED WRITING FILE")

		# return the binary filename
		return Response(status=status.HTTP_200_OK)


# generate authentication options
@api_view(['GET', 'POST'])
def handler_generate_authentication_options(requests):
	
	# read users login username from registration_login file
	print("opening")
	with open("/home/runner/bn-s/apis/login_username_file.txt", "r") as username_file:
		username = username_file.read()
		print(f"username: {username}")
		# if username is found in the file
		if username:
			# check if username is in database
			if User.objects.filter(username=username):
				
				user = User.objects.get(username = username)
				print(f"USER.CREDENTIALS: {user.credentials}")
				print(f"username: {user.username}")
				user_cred = UserCredential()
	# global current_authentication_challenge

	# generating authentication options
	options = generate_authentication_options(
        rp_id=RP_ID,
        allow_credentials=[{
            "type": "public-key",
            "id": user_cred.credential_id,
            "transports": ['internal', 'nfc', 'ble', 'usb']
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

#######################################################	
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