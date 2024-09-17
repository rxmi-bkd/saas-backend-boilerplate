from django.urls import path

from jwt_auth import views

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register, name='register'),
    path('update/password/', views.update_password, name='update_password'),
    path('update/user/', views.update_user, name='update_user'),
    path('reset/password/', views.reset_password, name='reset_password'),
    path('whoami/', views.who_am_i, name='who_am_i'),
]
