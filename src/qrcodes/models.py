from django.db import models
from shared.models import User


class QRCode(models.Model):
    url = models.URLField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, related_name='qrcodes', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
