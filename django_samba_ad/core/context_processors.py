from django.conf import settings


def server_information_processor(request):
    context = {
        'SAMBA_SERVER_IP': settings.SAMBA_SERVER_IP,
        'SAMBA_SERVER_PORT': settings.SAMBA_SERVER_PORT,
    }
    return context