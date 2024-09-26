from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from shared.serializers import UserSerializer, StandardizedErrorSerializer, UpdateUserSerializer, PasswordSerializer


@extend_schema(
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
    summary='Retrieve the informations of the authenticated user',
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
    request=PasswordSerializer,
    responses={
        HTTP_200_OK: UserSerializer,
        HTTP_400_BAD_REQUEST: StandardizedErrorSerializer,
        HTTP_401_UNAUTHORIZED: StandardizedErrorSerializer,
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = PasswordSerializer(request.user, data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(UserSerializer(user).data, status=HTTP_200_OK)


@extend_schema(
    request=UpdateUserSerializer,
    responses={
        HTTP_200_OK: UserSerializer,
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
    return Response(UserSerializer(user).data, status=HTTP_200_OK)
