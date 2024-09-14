from .models import CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=30)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
