from subprocess import PIPE, Popen
from time import sleep
import traceback
import logging as log

log.basicConfig(format="[%(levelname)s] -- %(message)s", level=log.INFO)
logger = log.getLogger(__name__)

class OdooSshShell:

    def __init__(self, ssh_url, shell):
        self.ssh_url = ssh_url
        self.shell = shell
        
    def __enter__(self):
        self.create_connection()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            # return False # uncomment to pass exception through
        self.close_connection

    def create_connection(self):
        self.proc = Popen(self.shell, stdin=PIPE, universal_newlines=True) 
        log.info(f'Connecting to  ::  {self.url}...\nUsing  ::  {self.shell}')
        self.write(f'ssh {self.ssh_url} -tt')

    def write(self, command, delay=1):
        log.info(f"Executing   ::  {command}")
        self.proc.stdin.write(f"{command}\n")
        self.proc.stdin.flush()
        sleep(delay)

    def restart_odoo(self):
        self.write('odoosh-restart')

    def psql_connect(self):
        self.write("psql")

    def write_sql(self, query):
        self.write(query)

    def close_connection(self):
        log.info("Closing Connection")
        self.proc.stdin.close()
        self.proc.wait()

