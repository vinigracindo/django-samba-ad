import socket
from django.conf import settings
from django.shortcuts import render

from django_samba_ad.ad.classes import SSHActiveDirectoryAccessModel
from django_samba_ad.core.models import User


def online_server_required(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        active_directory = settings.STRATEGY_AD_MODEL(
            settings.SAMBA_SERVER_IP,
            settings.SAMBA_SERVER_PORT,
            settings.SAMBA_ADMIN_USER,
            settings.SAMBA_ADMIN_PASSWORD
        )

        if not active_directory.is_online():
            return render(request, 'offline.html')

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware