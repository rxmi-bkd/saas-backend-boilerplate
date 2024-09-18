from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=30, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'])
        return user

    def update(self, instance, validated_data):
        user = User.objects.update_user(instance, **validated_data)
        return user
