import jwt

from shared.models import User
from django.conf import settings
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.decorators import api_view, permission_classes
from jwt_auth.utils import get_reset_token, send_password_reset_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from jwt_auth.serializers import ResetPasswordSerializer, ResetPasswordConfirmSerializer
from shared.serializers import UserSerializer, StandardizedErrorSerializer, UpdateUserSerializer, UpdatePasswordSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND


@extend_schema(
    summary='Register a new user',
    description='Register a new user and return JWT tokens (refresh and access).',
    request=UserSerializer,
    responses={
        HTTP_201_CREATED: TokenObtainPairSerializer,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
    }
)
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    token = RefreshToken.for_user(user)
    token = {'refresh': str(token), 'access': str(token.access_token)}

    return Response(token, status=HTTP_201_CREATED)


@extend_schema(
    summary='Get current user details',
    responses={
        HTTP_200_OK: UserSerializer,
        HTTP_401_UNAUTHORIZED: StandardizedErrorSerializer,
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def who_am_i(request):
    serializer = UserSerializer(request.user)

    return Response(serializer.data, status=HTTP_200_OK)


@extend_schema(
    summary='Update user password',
    description="Update the authenticated user's password.",
    request=UpdatePasswordSerializer,
    responses={
        HTTP_200_OK: None,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_401_UNAUTHORIZED: StandardizedErrorSerializer,
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = UpdatePasswordSerializer(request.user, data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(status=HTTP_200_OK)


@extend_schema(
    summary='Update user profile',
    description="Update the authenticated user's profile information.",
    request=UpdateUserSerializer,
    responses={
        HTTP_200_OK: None,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_401_UNAUTHORIZED: StandardizedErrorSerializer,
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    serializer = UpdateUserSerializer(request.user, data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(status=HTTP_200_OK)


@extend_schema(
    summary='Request password reset',
    description='Request a password reset for a user by providing their email address.',
    request=ResetPasswordSerializer,
    responses={
        HTTP_200_OK: None,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_404_NOT_FOUND: StandardizedErrorSerializer,
        HTTP_500_INTERNAL_SERVER_ERROR: StandardizedErrorSerializer,
    }
)
@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user = User.objects.get(email=serializer.validated_data['email'])
    except User.DoesNotExist:
        raise NotFound({'email': 'This email does not exist.'})

    reset_token = get_reset_token(serializer.validated_data['email'], settings.SECRET_KEY)

    status_code, response = send_password_reset_email(serializer.validated_data['email'], reset_token)

    if status_code != HTTP_200_OK:
        return Response({'error': 'An error occurred while sending the email. Please try again later.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=HTTP_200_OK)


@extend_schema(
    summary='Confirm password reset',
    description='Confirm a password reset using a token sent via email.',
    request=ResetPasswordConfirmSerializer,
    responses={
        HTTP_200_OK: None,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_404_NOT_FOUND: StandardizedErrorSerializer,
    }
)
@api_view(['PUT'])
def reset_password_confirm(request):
    serializer = ResetPasswordConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        payload = jwt.decode(serializer.validated_data['token'], settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ValidationError({'token': 'This token has expired.'})
    except jwt.InvalidTokenError:
        raise ValidationError({'token': 'This token is invalid.'})

    try:
        user = User.objects.get(email=payload['email'])
    except User.DoesNotExist:
        raise NotFound({'email': 'This email does not exist.'})

    user.set_password(serializer.validated_data['password'])
    user.save()

    return Response(status=HTTP_200_OK)
