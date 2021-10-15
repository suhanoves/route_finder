#!/bin/bash

python manage.py migrate
python manage.py loaddata ./fixtures/dump.json
#gunicorn project.wsgi:application --bind 0.0.0.0:8000

exec "$@"