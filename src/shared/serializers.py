from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=30, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=30)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UpdateUserSerializer(UserSerializer):
    password = None

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField()
    attr = serializers.CharField()


class StandardizedErrorSerializer(serializers.Serializer):
    type = serializers.CharField()
    errors = ErrorSerializer(many=True)
