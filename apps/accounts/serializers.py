from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'phone', 'avatar_url', 'commission_rate']
        read_only_fields = ['id', 'role']

class VerifyPinSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=6)

