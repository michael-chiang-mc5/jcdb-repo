#!/bin/bash

python manage.py collectstatic
pkill -f /home/michaelc/dev/mcatdb-repo/venv/bin/gunicorn
# python manage.py migrate --run-syncdb
gunicorn mySite.wsgi --bind 127.0.0.1:8002 --daemon --log-file ~/dev/logs/mcatdb.log --workers=1
