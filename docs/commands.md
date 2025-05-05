# ReviewApp - Commands utils

## Table of contents

- [Migrations](#make-migrations)
- [Migrate](#migrate-migrations)


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