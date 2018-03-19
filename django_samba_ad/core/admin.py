from django.contrib import admin

# Register your models here.
from django_samba_ad.core.models import User

admin.site.register(User)
