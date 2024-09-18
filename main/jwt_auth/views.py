from django.db.utils import IntegrityError

from shared.serializers import UserSerializer

from jwt_auth.serializers import UpdateUserFieldsSerializer, UpdateUserPasswordSerializer

from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST)
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


@extend_schema(
    description='Register a new user.',
    request=UserSerializer,
    responses={
        201: TokenObtainPairSerializer,
    },
)
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()

    token = RefreshToken.for_user(user)

    token = {'refresh': str(token), 'access': str(token.access_token)}

    return Response(token, status=HTTP_201_CREATED)


@extend_schema(
    description='Get information about the current user.',
    responses={
        200: UserSerializer
    },
)
@api_view()
@permission_classes([IsAuthenticated])
def who_am_i(request):
    serializer = UserSerializer(request.user)

    return Response(serializer.data, status=HTTP_200_OK)


@extend_schema(
    description="Update user's password.",
    request=UpdateUserPasswordSerializer,
    responses={
        200: UserSerializer
    },
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = UpdateUserPasswordSerializer(request.user, data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()
    serializer = UserSerializer(user)

    return Response(serializer.data, status=HTTP_200_OK)


@extend_schema(
    description="Update user's informations.",
    request=UpdateUserFieldsSerializer,
    responses={
        200: UserSerializer
    },
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    serializer = UpdateUserFieldsSerializer(request.user, data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    try:
        user = serializer.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
    except IntegrityError:
        errors = {'email': ['A user with that email already exists.']}
        return Response(errors, status=HTTP_400_BAD_REQUEST)


@extend_schema(
    description='Reset user password.',
    request=UserSerializer,
)
@api_view(['GET'])
def reset_password(request):
    return Response({'TODO': 'TODO'})
