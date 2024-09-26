from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from session_auth.serializers import LoginSerializer
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from shared.serializers import UserSerializer, StandardizedErrorSerializer, UpdateUserSerializer, PasswordSerializer


@extend_schema(
    request=UserSerializer,
    responses={
        HTTP_201_CREATED: UserSerializer,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
    }
)
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(UserSerializer(user).data, status=HTTP_201_CREATED)


@extend_schema(
    summary='Retrieve the information of the authenticated user',
    responses={
        HTTP_200_OK: UserSerializer,
        HTTP_403_FORBIDDEN: StandardizedErrorSerializer,
    }
)
@api_view()
@permission_classes([IsAuthenticated])
def who_am_i(request):
    serializer = UserSerializer(request.user)

    return Response(serializer.data, status=HTTP_200_OK)


@extend_schema(
    request=LoginSerializer,
    responses={
        HTTP_200_OK: UserSerializer,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_403_FORBIDDEN: StandardizedErrorSerializer,
    }
)
@sensitive_post_parameters()
@csrf_protect
@never_cache
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(request, **serializer.validated_data)

    if user is None:
        raise AuthenticationFailed()

    auth_login(request, user)

    return Response(UserSerializer(user).data, status=HTTP_200_OK)


@extend_schema(
    responses={
        HTTP_200_OK: None,
        HTTP_403_FORBIDDEN: StandardizedErrorSerializer,
    }
)
@csrf_protect
@api_view(['POST'])
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return Response(status=HTTP_200_OK)

    raise NotAuthenticated(detail='Impossible to log out an unauthenticated user.')


@extend_schema(
    request=PasswordSerializer,
    responses={
        HTTP_200_OK: None,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_403_FORBIDDEN: StandardizedErrorSerializer,
    }
)
@csrf_protect
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = PasswordSerializer(request.user, data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(status=HTTP_200_OK)


@extend_schema(
    request=UpdateUserSerializer,
    responses={
        HTTP_200_OK: UserSerializer,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_403_FORBIDDEN: StandardizedErrorSerializer,
    }
)
@csrf_protect
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    serializer = UpdateUserSerializer(request.user, data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(UserSerializer(user).data, status=HTTP_200_OK)
