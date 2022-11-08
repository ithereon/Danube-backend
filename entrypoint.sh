#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runworker
daphne -b 0.0.0.0 -p $PORT danube.asgi:application
