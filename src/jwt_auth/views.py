from django.db.utils import IntegrityError
from rest_framework.response import Response
from jwt_auth.utils import get_token_for_user
from jwt_auth.serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from jwt_auth.serializers import UpdateUserFieldsSerializer
from jwt_auth.serializers import UpdateUserPasswordSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK



@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()

    return Response(get_token_for_user(user), status=HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = UpdateUserPasswordSerializer(request.user, data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = serializer.save()

    return Response(status=HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    serializer = UpdateUserFieldsSerializer(request.user, data=request.data)

    if serializer.is_valid() is False:
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    try:
        serializer.save()
        return Response(status=HTTP_200_OK)
    except IntegrityError:
        errors = {"email": ["A user with that email already exists."]}
        return Response(errors, status=HTTP_400_BAD_REQUEST)

# TODO: password reset