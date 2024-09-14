from jwt_auth.models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from jwt_auth.serializers import CustomUserSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST


@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        CustomUser.objects.create_user(serializer.validated_data['email'], serializer.validated_data['password'])

        return Response(serializer.validated_data, status=HTTP_201_CREATED)

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# TODO: password change, password reset, email change