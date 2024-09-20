import jwt
from shared.models import User
from django.conf import settings
from django.db.utils import IntegrityError
from rest_framework.response import Response
from shared.serializers import UserSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from jwt_auth.utils import get_reset_token, send_password_reset_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from jwt_auth.serializers import UpdateUserSerializer, UpdatePasswordSerializer, ResetPasswordSerializer, ResetPasswordConfirmSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR


@extend_schema(description='Register a new user.', request=UserSerializer,
               responses={HTTP_201_CREATED: TokenObtainPairSerializer, HTTP_400_BAD_REQUEST: 'Bad request'}, )
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()

    token = RefreshToken.for_user(user)

    token = {'refresh': str(token), 'access': str(token.access_token)}

    return Response(token, status=HTTP_201_CREATED)


@extend_schema(description='Get information about the current user.',
               responses={HTTP_200_OK: UserSerializer, HTTP_401_UNAUTHORIZED: 'Unauthorized'}, )
@api_view()
@permission_classes([IsAuthenticated])
def who_am_i(request):
    serializer = UserSerializer(request.user)

    return Response(serializer.data, status=HTTP_200_OK)


@extend_schema(description="Update user's password.", request=UpdatePasswordSerializer,
               responses={HTTP_200_OK: '', HTTP_400_BAD_REQUEST: 'Bad request',
                          HTTP_401_UNAUTHORIZED: 'Unauthorized'}, )
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = UpdatePasswordSerializer(request.user, data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()

    return Response(status=HTTP_200_OK)


@extend_schema(description="Update user's informations.", request=UpdateUserSerializer,
               responses={HTTP_200_OK: UserSerializer, HTTP_400_BAD_REQUEST: 'Bad request',
                          HTTP_401_UNAUTHORIZED: 'Unauthorized'}, )
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    serializer = UpdateUserSerializer(request.user, data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    try:
        user = serializer.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
    except IntegrityError:
        errors = {'email': ['A user with that email already exists.']}
        return Response(errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response('No user with that email.', status=HTTP_400_BAD_REQUEST)

    reset_token = get_reset_token(email, settings.SECRET_KEY)

    status_code, response = send_password_reset_email(email, reset_token)

    if status_code != 200:
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=HTTP_200_OK)


@api_view(['PUT'])
def reset_password_confirm(request):
    serializer = ResetPasswordConfirmSerializer(data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    token = serializer.validated_data['token']
    password = serializer.validated_data['password']

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response('Token expired.', status=HTTP_400_BAD_REQUEST)
    except jwt.InvalidTokenError:
        return Response('Invalid token.', status=HTTP_400_BAD_REQUEST)

    email = payload['email']

    user = User.objects.get(email=email)
    user.set_password(password)

    user = user.save()

    return Response(status=HTTP_200_OK)
