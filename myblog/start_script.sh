#!/bin/bash

# application settings
export DJANGO_SETTINGS_MODULE=HelloWorld.settings
echo `pwd`
echo `ls`
cd HelloWorld
./manage.py migrate --noinput
./manage.py loaddata /data/django/superuser/superuser.json
# ./manage.py runserver 0.0.0.0:8088

cd ..
uwsgi --ini /data/django/www/mblog/uwsgi.ini
