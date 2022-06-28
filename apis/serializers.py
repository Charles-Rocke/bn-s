from rest_framework import serializers
from users.models import User

# serializers here
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {"displayname", "username"}