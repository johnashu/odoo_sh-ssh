from subprocess import PIPE, Popen
from time import sleep

class OdooSsh:

    def __init__(self, ssh_url, shell):
        self.ssh_url = ssh_url
        self.proc = Popen(shell, stdin=PIPE, universal_newlines=True)
        self.create_connection()

    def create_connection(self):
        self.write(f'ssh {self.ssh_url} -tt')

    def write(self, data, delay=1):
        self.proc.stdin.write(f"{data}\n")
        self.proc.stdin.flush()
        sleep(delay)

    def restart_odoo(self):
        self.write('odoosh-restart')

    def psql_connect(self):
        self.write("psql")

    def write_sql(self, query):
        self.write(query)

    def close_connection(self):
        self.proc.stdin.close()
        self.proc.wait()


url = '12345@company_name.odoo.com'
shell = 'cmd.exe' # 'sh' # 'bash'
q = 'select name from stock_production_lot where id=1;'

ossh = OdooSsh(url, shell)

try:    
    ossh.restart_odoo()
    ossh.psql_connect()
    ossh.write_sql(q)
finally:
    ossh.close_connection()
