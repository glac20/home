net153
==============================

Net153 Home

A migration of a [blosxom](http://www.blosxom.com/) ( [mirror](https://web.archive.org/web/20210308071735/https://www.blosxom.com/) ) powered blog converted to a Django project.

### Quick setup

> The next steps assume that conda is already installed

1 - <a name="step-1">Install the project basic dependencies and development dependencies</a>

> Make sure you are inside the root project directory before executing the next commands.
>
> The root project directory is the directory that contains the `manage.py` file

On Linux and Mac

```bash
pip install -r requirements/local.txt
```

On Windows

```bash
pip install -r requirements\local.txt
```

2 - <a name="step-2">Configure the database connection string on the .env</a>

On Linux and Mac

```bash
cp env.sample.mac_or_linux .env
```

On Windows

```bash
copy env.sample.windows .env
```

Change the value of the variable `DATABASE_URL` inside the file` .env` with the information of the database we want to connect.

Note: Several project settings have been configured so that they can be easily manipulated using environment variables or a plain text configuration file, such as the `.env` file.
This is done with the help of a library called django-environ. We can see the formats expected by `DATABASE_URL` at https://github.com/jacobian/dj-database-url#url-schema. 

3 - <a name="step-3">Use the django-extension's `sqlcreate` management command to help to create the database</a>

On Linux:

```bash
python manage.py sqlcreate | sudo -u postgres psql -U postgres
```

On Mac:

```bash
python manage.py sqlcreate | psql
```

On Windows:

Since [there is no official support for PostgreSQL 12 on Windows 10](https://www.postgresql.org/download/windows/) (officially PostgreSQL 12 is only supported on Windows Server), we choose to use SQLite3 on Windows

4 - <a name="step-4">Run the `migrations` to finish configuring the database to able to run the project</a>


```bash
python manage.py migrate
```


### <a name="running-tests">Running the tests and coverage test</a>


```bash
coverage run -m pytest
```
