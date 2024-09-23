from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings

if settings.AUTH_TYPE == 'JWT':
    auth_path = path('jwt/', include('jwt_auth.urls'))
elif settings.AUTH_TYPE == 'SESSION':
    auth_path = path('session/', include('session_auth.urls'))
else:
    raise ValueError('AUTH_TYPE must be either "JWT" or "SESSION')

urlpatterns = [
    path('', lambda request: redirect('docs/', permanent=True)),
    path('admin/', admin.site.urls),
    auth_path,
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]


