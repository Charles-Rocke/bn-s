from django.db import models
from webauthn.helpers.structs import AuthenticatorTransport
from typing import Optional, List
from dataclasses import dataclass, field

@dataclass
class Credential:
    id: bytes
    public_key: bytes
    sign_count: int
    transports: Optional[List[AuthenticatorTransport]] = None


@dataclass
class UserAccount:
    id: str
    username: str
    credentials: List[Credential] = field(default_factory=list)
    
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    credentials = models.TextField()
    
    def __str__(self):
        return self.username

# table for user credentials
class Credentials(models.model):
	id = models.BinaryField()
	public_key = models.BinaryField()
	sign_count = models.IntegerField()
	transports: Optional[List[AuthenticatorTransport]] = None