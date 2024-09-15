from tkinter.font import names
from jwt_auth.models import CustomUser
from jwt_auth.serializers import CustomUserSerializer
from rest_framework.generics import ListAPIView

from jwt_auth import views

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('register/', views.register, name='register'),
    path('update/password/', views.update_password, name='update_password'),
    path('update/user/', views.update_user, name='update_user'),
    path('users/', ListAPIView.as_view(queryset=CustomUser.objects.all(), serializer_class=CustomUserSerializer), name='users')
]
