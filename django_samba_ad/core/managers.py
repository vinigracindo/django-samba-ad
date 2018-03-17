from django.db import models
from django.conf import settings
import paramiko
import re
import time


class UserModelManager(models.Manager):
    def get_queryset(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(settings.SAMBA_SERVER_IP,
                       username=settings.SAMBA_ADMIN_USER,
                       password=settings.SAMBA_ADMIN_PASSWORD,
                       allow_agent=True)

        command = "sudo pdbedit -L -v"
        stdin, stdout, stderr = client.exec_command(command)
        entries = stdout.read().decode('utf-8', errors='replace').split('-' * 15)
        entries = list(filter(None, entries))
        users = []
        for entry in entries:
            print(entry)
            username = re.search('Unix username:(.*)\\n', entry).group(1).strip()
            print(username)
            # Not is computer name.
            if username.find('$') == -1:
                fullname = re.search('Full Name:(.*)\\n', entry).group(1).strip()
                logontime = re.search('Logon time:(.*)\\n', entry).group(1).strip()
                user = {'username': username, 'fullname': fullname, 'last_logon': logontime}
                users.append(user)

        client.close()

        return users