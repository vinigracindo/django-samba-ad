from django.conf import settings

from django_samba_ad.core.models import User


def synchronize_user(function):
    def wrap(request, *args, **kwargs):
        active_directory = settings.STRATEGY_AD_MODEL(
            settings.SAMBA_SERVER_IP,
            settings.SAMBA_SERVER_PORT,
            settings.SAMBA_ADMIN_USER,
            settings.SAMBA_ADMIN_PASSWORD,
        )

        # sync
        users = active_directory.retrieve_users()
        for user in users:
            User.objects.update_or_create(username=user['username'], defaults=user)
        # end sync

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap