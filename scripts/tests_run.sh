#!/bin/sh
while ! nc -z postgres 5432; do sleep 5; done
python manage.py migrate
sleep 5

pytest tests