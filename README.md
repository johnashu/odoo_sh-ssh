# odoo_sh-ssh
Class to connect and control Odoo sh Shell

It is assumed that all SSH keys are already setup

### 1. Select the SSh address found on Odoo.sh and add as url
### 2. Choose Shell for the system you are using

url = '12345@company.odoo.com'
shell = 'cmd.exe' # 'sh' # 'bash'

### example SQL query
q = 'select name from stock_production_lot where id=1;'

# examples
### Use a try/finally with optional except / else if neededs
```python
ossh = OdooSsh(url, shell)

try:    
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

### Use a context manager to handle the above for you
```python
with OdooSsh(url, shell) as ossh:
    ossh.restart_odoo()
    ossh.psql_connect()
    ossh.write_sql(q)
```