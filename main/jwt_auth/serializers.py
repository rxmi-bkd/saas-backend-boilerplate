from rest_framework import serializers


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=30)
