from django.db import models
from django.conf import settings
import paramiko
import re
import time


class UserModelManager(models.Manager):
    def get_queryset(self):
        active_directory = settings.STRATEGY_AD_MODEL(
            settings.SAMBA_SERVER_IP,
            settings.SAMBA_SERVER_PORT,
            settings.SAMBA_ADMIN_USER,
            settings.SAMBA_ADMIN_PASSWORD,
        )

        return active_directory.retrieve_users()