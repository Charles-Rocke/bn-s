from django.conf import settings
from django.db import models


# Create your models here
# specific user credential
class UserCredential(models.Model):
	id = models.BinaryField(primary_key = True, unique = True)
	credential_id = models.BinaryField()
	public_key = models.BinaryField()
	sign_count = models.PositiveBigIntegerField()
	transports = models.CharField(max_length=20)
	username = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )