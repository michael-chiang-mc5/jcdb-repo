#!/bin/bash
#!/bin/bash

python manage.py migrate --run-syncdb
python manage.py makemigrations
python manage.py migrate
