import traceback
import os
import paramiko
from time import sleep
import logging as log

log.basicConfig(format="[%(levelname)s] -- %(message)s", level=log.INFO)
logger = log.getLogger(__name__)


class OdooSshPara:
    def __init__(self, ssh_url, user, key_file):
        self.ssh_url = ssh_url
        self.user = user
        self.key_file = key_file
        self.SSH_KEY = paramiko.RSAKey.from_private_key_file(self.key_file)

    def __enter__(self):
        """ With Context start """
        self.create_connection()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        """ With Context cleanup / error handling/ finish """
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            # return False # uncomment to pass exception through
        self.close_connection

    def create_connection(self):
        """Create a connection object
        """
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        log.info("connecting")
        self.ssh.connect(
            self.ssh_url, username=self.user, pkey=self.SSH_KEY,
        )

    def write(self, command, delay=1):
        """ write commands to the shell that is open """
        log.info(f"Executing {command}")
        stdin, stdout, stderr = self.ssh.exec_command(command, timeout=5)
        out, err = str(stdout.read(), "ascii"), str(stderr.read(), "ascii")
        sleep(delay)
        return out, err

    def restart_odoo(self):
        """ Restart Odoo.sh Workers"""
        res = self.write("odoosh-restart")
        return res

    def close_connection(self):
        """ close connection gracefully """
        log.info("Closing Connection")
        self.ssh.close()
