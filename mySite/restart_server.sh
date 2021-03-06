#!/bin/bash

python manage.py collectstatic
pkill -f /home/michaelc/dev/jcdb-repo/venv/bin/gunicorn
# python manage.py migrate --run-syncdb
gunicorn mySite.wsgi --bind 127.0.0.1:8003 --daemon --log-file ~/dev/logs/jcdb.log --workers=1
