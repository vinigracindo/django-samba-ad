import re

import paramiko

from django_samba_ad.ad.base import BaseActiveDirectoryAccessModel
import socket


class SSHActiveDirectoryAccessModel(BaseActiveDirectoryAccessModel):
    def connect(self):
        pass

    def disconnect(self):
        pass

    def is_online(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # The error indicator is 0 if the operation succeeded, otherwise the value of the errno variable
        result = sock.connect_ex((self.server_ip, self.server_port))
        is_online_server = True if (result == 0) else False

        return is_online_server

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