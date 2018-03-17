"""
Base Active Directory Access Models.
"""

# Author: Vinnicyus Gracindo
# License: BSD


class BaseActiveDirectoryAccessModel(object):
    def __init__(self, server_ip, server_port, admin_user, admin_password):
        self.server_ip = server_ip
        self.server_port = server_port
        self.admin_user = admin_user
        self.admin_password = admin_password

    def connect(self):
        pass

    def disconnect(self):
        pass

    def is_online(self):
        pass

    def retrieve_users(self):
        pass