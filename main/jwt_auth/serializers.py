from shared.models import User

from rest_framework import serializers


class UpdateUserSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        user = User.objects.update_user(instance, **validated_data)
        return user


class UpdateUserPasswordSerializer(UpdateUserSerializer):
    password = serializers.CharField(min_length=8, max_length=30)


class UpdateUserFieldsSerializer(UpdateUserSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)  # If you need to update other fields. Add them here
