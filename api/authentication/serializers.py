from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ChangeLoginSerializer(serializers.Serializer):
    new_username = serializers.CharField(required=True)
