#!/bin/sh
python manage.py migrate
gunicorn 'pysat.wsgi' -b 0.0.0.0:3027 --access-logfile - --log-level info
