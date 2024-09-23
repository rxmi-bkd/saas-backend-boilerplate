from jwt_auth import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='jwt_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),
    path('register/', views.register, name='jwt_register'),
    path('update/password/', views.update_password, name='jwt_update_password'),
    path('update/user/', views.update_user, name='jwt_update_user'),
    path('reset/password/', views.reset_password, name='jwt_reset_password'),
    path('reset/password/confirm/', views.reset_password_confirm, name='jwt_reset_password_confirm'),
    path('whoami/', views.who_am_i, name='jwt_who_am_i'),
]
