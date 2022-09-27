from django.conf import settings
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser


# Create your models here
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
	User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )