from .models import CustomUser

from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=30, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data['email'],
                                              password=validated_data['password'],
                                              first_name=validated_data['first_name'],
                                              last_name=validated_data['last_name'])
        return user

    def update(self, instance, validated_data):
        user = CustomUser.objects.update_user(instance, **validated_data)
        return user


class UpdateUserSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        user = CustomUser.objects.update_user(instance, **validated_data)
        return user


class UpdateUserPasswordSerializer(UpdateUserSerializer):
    password = serializers.CharField(min_length=8, max_length=30)


class UpdateUserFieldsSerializer(UpdateUserSerializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)  # If you need to update other fields. Add them here
