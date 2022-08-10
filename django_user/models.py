from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
# specific user credential
class UserCredential(models.Model):
	id = models.BinaryField(primary_key = True, unique = True)
	credential_id = models.BinaryField()
	public_key = models.BinaryField()
	sign_count = models.PositiveBigIntegerField()
	transports = models.CharField(max_length=20)
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)