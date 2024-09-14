from jwt_auth import views

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # this endpoint act as login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register)
]
