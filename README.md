# `generate_sql_script.py`

This script generates a SQL script based on a Jinja2 template, allowing you to automate the creation of a database, roles, and permissions. It is particularly useful for setting up a PostgreSQL database with predefined roles and permissions.

## Usage

```bash
docker run -v $PWD:/app -w /app --rm --name sqlgen pledo/sql-script-generator -d <database_name> -w <readwrite_role> -u <user_role> -p <password> -t <template_file> -o <output_file>
-d, --database: Name of the database.
-w, --readwrite_role: Name of the readwrite role.
-u, --user_role: Name of the users role.
-p, --password: Password for the user roles.
-t, --template: Path to the Jinja2 template file.
-o, --output_file: Output file for the generated SQL script.
```

Docker Tests


Install postgresql-client:
```bash
$ sudo apt install postgresql-client
```

Start the PostgreSQL container:
```bash
$ sudo docker run --name psql-validating -e POSTGRES_PASSWORD=mysecretpassword -p 5555:5432 -d postgres:13
```

Run generate_sql_script.py:
```bash
$ docker run -v $PWD:/app -w /app --rm --name sqlgen pledo/sql-script-generator -d test -w test_readwrite -u test_user -p 'qweasdzxc' -t readwrite-user-template.sql.j2 -o test_sql_script.sql
```

Run the generated SQL script:
```bash
$ export PGPASSWORD='mysecretpassword'; psql -h localhost -U postgres -d postgres -p 5555 -w -f test_sql_script.sql

CREATE DATABASE
CREATE ROLE
GRANT
GRANT
GRANT
GRANT
GRANT
GRANT
GRANT
ALTER DEFAULT PRIVILEGES
ALTER DEFAULT PRIVILEGES
ALTER DEFAULT PRIVILEGES
CREATE ROLE
GRANT ROLE
ALTER DATABASE

```

Run user commands to test write operations 
```bash
$ export PGPASSWORD='qweasdzxc'; psql -h localhost -U test_user -d test -p 5555 -w -c 'create table IF NOT EXISTS tabela1 (coluna1 VARCHAR(50) UNIQUE NOT NULL, coluna2 VARCHAR(50));'

CREATE TABLE
```

Testing read operations:

```bash
$ export PGPASSWORD='qweasdzxc'; psql -h localhost -U test_user -d test -p 5555 -w -c 'select * from tabela1;'

 coluna1 | coluna2 
---------+---------
(0 rows)

```

Update operations:

```bash
$ export PGPASSWORD='qweasdzxc'; psql -h localhost -U test_user -d test -p 5555 -w -c 'alter table public.tabela1 ADD COLUMN coluna3 varchar(50);'
ALTER TABLE


$ export PGPASSWORD='qweasdzxc'; psql -h localhost -U test_user -d test -p 5555 -w -c 'select * from tabela1;'
 coluna1 | coluna2 | coluna3 
---------+---------+---------
(0 rows)
```

Removing the Docker container:

```bash
sudo docker stop psql-validating; sudo docker rm psql-validating
```
