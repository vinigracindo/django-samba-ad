from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    fullname = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)
    enable = models.BooleanField(default=True)
    last_logon = models.CharField(max_length=100, blank=True, null=True, editable=False)
    change_password_next_logon = models.BooleanField(default=False)
    disable_account = models.BooleanField(default=False)

    def __str__(self):
        return self.username