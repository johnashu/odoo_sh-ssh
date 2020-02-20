# odoo_sh-ssh
Class to connect and control Odoo sh Shell using Os shell or Paramiko library

The Shell option allows you to quickly establish an interactive login to the Psql shell

for example:

```python
ossh  = OdooSshShell(url, shell)
ossh.create_connection()
ossh.psql_connect()
while True:
    i = input()
    ossh.write(i)

```
```bash

psql (10.8, server 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1))
SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
Type "help" for help.

company-master-123456=> select name from stock_production_lot where id=1;

             name
-------------------------------
 product_1234567890
(1 row)

company-master-123456=>
...


# Shell Based (CMD, Bash, SH)
It is assumed that all SSH keys are already setup .

### 1. Select the SSh address found on Odoo.sh and add as url
### 2. Choose Shell for the system you are using

url = '12345@company.odoo.com' 

shell = 'cmd.exe' # 'sh' # 'bash'

### Example SQL query
q = 'select name from stock_production_lot where id=1;'

# examples
### Use a try/finally with optional except / else if needed
```python
ossh = OdooSshShell(url, shell)

try:
    ossh.create_connection()    
    ossh.restart_odoo()
    ossh.psql_connect()
    ossh.write_sql(q)
except SomeException as e:
    handle_exception()
else:
    do_something()
finally:
    ossh.close_connection()

```

### Use context manager to do this for you.
```python
    with OdooSshShell(url, shell) as ossh:
        ossh.restart_odoo()
        ossh.psql_connect()
        ossh.write_sql(q)
```

# Use Paramiko to connect
URL = "company.odoo.com"
USER = "123456"
KEY_FILE = "path/to/ssh_key"


```python
ossh = OdooSshPara(URL, USER, KEY_FILE)

c = 'psql -qAtX -c "select  name from stock_production_lot where id in (1, 2, 3, 4);"'

try:
    ossh.create_connection()
    ossh.restart_odoo()
    out, err = ossh.write(c)

    with open('test.csv', 'a') as f:
        f.write(out)

except KeyboardInterrupt as e:
    ossh.close_connection()
else:
    print("Something Else Happened...")
finally:
    ossh.close_connection()
```

### Use context manager to do this for you.
```python
with OdooSshPara(URL, USER, KEY_FILE) as ossh:
    res = ossh.restart_odoo()
    print(res)
```