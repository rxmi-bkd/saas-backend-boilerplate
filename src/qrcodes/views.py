from django.shortcuts import redirect

from .models import QRCode
from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet
from .serializers import QRCodeSerializer, UrlSerializer
from shared.serializers import StandardizedErrorSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND


class QRCodeViewSet(ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.filter(owner=self.request.user)

        return queryset

    @extend_schema(
        summary='Redirect to the URL associated with the QR code',
        responses={
            HTTP_200_OK: UrlSerializer,
            HTTP_404_NOT_FOUND: StandardizedErrorSerializer,
        }
    )
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def see(self, request, pk):
        try:
            qr_code = QRCode.objects.get(pk=pk)
            serializer = UrlSerializer(qr_code)

            return redirect(serializer.data['url'])
        except QRCode.DoesNotExist:
            raise NotFound()
