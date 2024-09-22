from shared.models import User
from rest_framework import serializers
from shared.serializers import UserSerializer


class UpdateUserSerializer(UserSerializer):
    password = None

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=30)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=30)
