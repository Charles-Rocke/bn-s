from webauthn.helpers.structs import AuthenticatorTransport
from typing import Optional, List
from dataclasses import dataclass, field
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models



# Create your models here.
# Credential
"""
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
"""
		

# specific user
class User(AbstractUser):
	id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique = True)
	username = models.CharField(max_length = 50, unique = True)

	def __str__(self):
		return self.username

# specific user credential
class UserCredential(models.Model):
	id = models.BinaryField(primary_key = True, unique = True)
	credential_id = models.BinaryField()
	public_key = models.BinaryField()
	sign_count = models.PositiveBigIntegerField()
	transports = models.CharField(max_length=20)
	user = models.ForeignKey(User, on_delete=models.CASCADE)