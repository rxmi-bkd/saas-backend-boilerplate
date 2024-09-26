import jwt

from shared.models import User
from django.conf import settings
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import NotFound, ValidationError
from reset_password.utils import get_reset_token, send_password_reset_email
from shared.serializers import EmailSerializer, StandardizedErrorSerializer, PasswordSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


@extend_schema(
    summary='Send password reset link via email',
    request=EmailSerializer,
    responses={
        HTTP_200_OK: None,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_404_NOT_FOUND: StandardizedErrorSerializer,
        HTTP_500_INTERNAL_SERVER_ERROR: StandardizedErrorSerializer,
    }
)
@api_view(['POST'])
def activate_reset_password(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user = User.objects.get(email=serializer.validated_data['email'])
    except User.DoesNotExist:
        raise NotFound({'email': 'This email does not exist.'})

    reset_token = get_reset_token(serializer.validated_data['email'], settings.SECRET_KEY)

    return Response({'token': reset_token}, status=HTTP_200_OK)
    """
    status_code, response = send_password_reset_email(serializer.validated_data['email'], reset_token)

    if status_code != HTTP_200_OK:
        return Response({'error': 'An error occurred while sending the email. Please try again later.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(status=HTTP_200_OK)
    """


@extend_schema(
    summary='Reset the password using the token sent via email',
    request=PasswordSerializer,
    responses={
        HTTP_200_OK: None,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_404_NOT_FOUND: StandardizedErrorSerializer,
    },
    parameters=[
        OpenApiParameter(
            name='token',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=True,
            description='The token sent via email to confirm the password reset.'
        )
    ]
)
@api_view(['PUT'])
def reset_password_confirm(request):
    token = request.query_params.get('token')

    if not token:
        raise ValidationError({'token': 'This parameter is required.'})

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ValidationError({'token': 'This token has expired.'})
    except jwt.InvalidTokenError:
        raise ValidationError({'token': 'This token is invalid.'})

    serializer = PasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user = User.objects.get(email=payload['email'])
    except User.DoesNotExist:
        raise NotFound({'email': 'This email does not exist.'})

    user.set_password(serializer.validated_data['password'])
    user.save()

    return Response(status=HTTP_200_OK)
