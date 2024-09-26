from .models import QRCode
from rest_framework import serializers


class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'url', 'created_at', 'updated_at', 'owner']

    owner = serializers.ReadOnlyField(source='owner.pk')


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField()
