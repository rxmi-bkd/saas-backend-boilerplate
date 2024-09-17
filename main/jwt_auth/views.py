from django.db.utils import IntegrityError

from jwt_auth.serializers import (CustomUserSerializer, UpdateUserFieldsSerializer, UpdateUserPasswordSerializer)

from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST)
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()

    token = RefreshToken.for_user(user)

    token = {'refresh': str(token), 'access': str(token.access_token)}

    return Response(token, status=HTTP_201_CREATED)


@api_view()
@permission_classes([IsAuthenticated])
def who_am_i(request):
    serializer = CustomUserSerializer(request.user)

    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = UpdateUserPasswordSerializer(request.user, data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()
    serializer = CustomUserSerializer(user)

    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    serializer = UpdateUserFieldsSerializer(request.user, data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    try:
        user = serializer.save()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)
    except IntegrityError:
        errors = {'email': ['A user with that email already exists.']}
        return Response(errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def reset_password(request):
    return Response({'TODO': 'TODO'})
