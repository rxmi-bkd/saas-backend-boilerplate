from django.db.utils import IntegrityError
from drf_spectacular.utils import extend_schema
from jwt_auth.serializers import UpdateUserSerializer, UpdatePasswordSerializer
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from shared.serializers import UserSerializer


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


@api_view(['GET'])
def reset_password(request):
    return Response({'TODO': 'TODO'})
