from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', lambda request: redirect('docs/', permanent=True)),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.AUTH_TYPE == 'JWT':
    urlpatterns += path('jwt/', include('jwt_auth.urls')),
    urlpatterns += path('reset/password/', include('reset_password.urls')),
elif settings.AUTH_TYPE == 'SESSION':
    urlpatterns += path('session/', include('session_auth.urls')),
    urlpatterns += path('reset/password/', include('reset_password.urls')),
elif settings.AUTH_TYPE == 'BOTH':
    urlpatterns += path('jwt/', include('jwt_auth.urls')),
    urlpatterns += path('session/', include('session_auth.urls')),
    urlpatterns += path('reset/password/', include('reset_password.urls')),
elif settings.AUTH_TYPE is None:
    pass
else:
    raise ValueError('Invalid value for AUTH_TYPE in settings.py')


