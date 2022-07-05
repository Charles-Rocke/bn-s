from rest_framework import serializers
from users.models import Users

# serializers here
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {"displayname", "username"}