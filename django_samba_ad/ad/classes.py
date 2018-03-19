import re
from time import sleep

import paramiko

from django_samba_ad.ad.base import BaseActiveDirectoryAccessModel
import socket

"""
Samba Account Flags
D	Account is disabled.
H	A home directory is required.
I	An inter-domain trust account.
L	Account has been auto-locked.
M	An MNS (Microsoft network service) logon account.
N	Password not required.
S	A server trust account.
T	Temporary duplicate account entry.
U	A normal user account.
W	A workstation trust account.
X	Password does not expire.
"""


class SSHActiveDirectoryAccessModel(BaseActiveDirectoryAccessModel):
    def connect(self):
        pass

    def disconnect(self):
        pass

    def is_online(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # The error indicator is 0 if the operation succeeded, otherwise the value of the errno variable
        result = sock.connect_ex((self.server_ip, self.server_port))

        return True if (result == 0) else False

    def update_user(self, user_attributes):
        print(user_attributes)
        username = user_attributes['username']
        fullname = user_attributes['fullname']
        description = user_attributes['description']
        enable = user_attributes['enable']
        change_password = user_attributes['change_password_next_logon']

        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(self.server_ip,
                       username=self.admin_user,
                       password=self.admin_password,
                       allow_agent=True)

        if change_password:
            command = 'sudo net sam set pwdmustchangenow {} yes'.format(username)
            client.exec_command(command)
            sleep(0.5)

        if not enable:
            command = 'sudo net sam set disable {} yes'.format(username)
        else:
            command = 'sudo net sam set disable {} no'.format(username)

        client.exec_command(command)
        sleep(0.5)

        command = 'sudo net sam set comment {} "{}"'.format(username, description)
        client.exec_command(command)
        sleep(0.5)
        command = 'sudo net sam set fullname {} "{}"'.format(username, fullname)
        client.exec_command(command)
        sleep(0.5)
        command = 'sudo net sam set pwd {} "{}"'.format(username, fullname)
        client.exec_command(command)
        sleep(0.5)

    def retrieve_users(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)
        client.connect(self.server_ip,
                       username=self.admin_user,
                       password=self.admin_password,
                       allow_agent=True)

        command = "sudo pdbedit -L -v"
        stdin, stdout, stderr = client.exec_command(command)
        entries = stdout.read().decode('utf-8', errors='replace').split('-' * 15)
        entries = list(filter(None, entries))
        users = []
        for entry in entries:
            username = re.search('Unix username:(.*)\\n', entry).group(1).strip()
            # Not is computer name.
            if username.find('$') == -1:
                fullname = re.search('Full Name:(.*)\\n', entry).group(1).strip()
                description = re.search('Account desc:(.*)\\n', entry).group(1).strip()
                logontime = re.search('Logon time:(.*)\\n', entry).group(1).strip()
                account_flags = re.search('Account Flags:(.*)\\n', entry).group(1).strip()
                user = {'username': username,
                        'description': description,
                        'fullname': fullname,
                        'enable': not account_flags.__contains__('D'),
                        'last_logon': logontime}
                users.append(user)

        client.close()

        return users

"""
    change_password_next_logon = models.BooleanField(default=False)
    disable_account = models.BooleanField(default=False)
"""