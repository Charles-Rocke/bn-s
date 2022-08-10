from webauthn.helpers.structs import AuthenticatorTransport
from typing import Optional, List
from dataclasses import dataclass, field

from django.contrib.auth import get_user_model
from django.db import models



# Create your models here.
# Credential

@dataclass
class Credential:
    id: bytes
    public_key: bytes
    sign_count: int
    transports: Optional[List[AuthenticatorTransport]] = None

    def __init__(self, id: bytes, public_key: bytes, sign_count: int, transports: Optional[List[AuthenticatorTransport]]):
	    self.id = id
	    self.public_key = public_key
	    self.sign_count = sign_count
	    self.tansports = transports

		
# UserAccount
@dataclass
class UserAccount:
    id: str
    username: str
    credentials: List[Credential] = field(default_factory=list)

    def __init__(self, id: str, username: str, credentials: List[Credential] = field(default_factory=list)):
	    self.id = id
	    self.username = username
	    self.credentials = credentials

