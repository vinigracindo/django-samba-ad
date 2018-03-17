import socket
from django.conf import settings
from django.shortcuts import render


def online_server_required(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((settings.SAMBA_SERVER_IP, settings.SAMBA_SERVER_PORT))
        is_online_server = True if (result == 0) else False

        if not is_online_server:
            return render(request, 'offline.html')

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware