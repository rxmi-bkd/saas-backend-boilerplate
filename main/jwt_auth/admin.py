from django.contrib import admin

from jwt_auth.models import CustomUser

admin.site.register(CustomUser)
