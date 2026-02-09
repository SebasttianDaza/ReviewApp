# ReviewApp - Commands utils

## Table of contents

- [Migrations](#make-migrations)
- [Migrate](#migrate-migrations)
- [Install Azure Storage Explorer](#install-azure-storage-explorer)
- [Upload files static storage](#upload-files-statics-to-storage)
- [Create user admin](#create-user-admin)


## Make migrations

```bash
$  python manage.py makemigrations publisher
```

## Migrate migrations

The sqlmigrate command doesn’t actually run the migration on your database - instead, it prints it to the screen so that you can see what SQL Django thinks is required. It’s useful for checking what Django is going to do or if you have database administrators who require SQL scripts for changes.

[Link docs](https://docs.djangoproject.com/en/5.0/ref/django-admin/#django-admin-sqlmigrate)

```bash
$ python manage.py sqlmigrate publisher 0001
```

```bash
$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./build/reviewapp.key -out ./build/reviewapp.crt -config ./build/reviewapp.conf -passin pass:reviewapppy

```

```bash
$  docker compose up -d --wait --remove-orphans
```

## Install Azure storage explorer

```bash
$ sudo apt update
$ sudo apt install snapd
$ sudo snap install storage-explorer
```

## Upload files statics to storage

[Docs](https://django-storages.readthedocs.io/en/latest/backends/azure.html)

```bash
$ python manage.py collectstatic
```

## Create user admin

```bash
$ python manage.py createsuperuser --username=joe --email=joe@example.com
# or
$ python manage.py createsuperuser
```