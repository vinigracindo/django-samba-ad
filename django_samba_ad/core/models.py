from django.db import models

from django_samba_ad.core.managers import UserModelManager


class User(models.Model):
    username = models.CharField(max_length=50)
    fullname = models.CharField(max_length=200)

    objects = UserModelManager()