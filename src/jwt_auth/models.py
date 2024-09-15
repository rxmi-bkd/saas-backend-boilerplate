from django.db import models
from jwt_auth.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(_("first name"), max_length=30)
    last_name = models.CharField(_("last name"), max_length=30)
    email = models.EmailField(_('email address'), unique=True, error_messages= {'unique': 'A user with that email already exists.'})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
