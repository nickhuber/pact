#!/usr/bin/env bash

set -e

echo "Ensuring virtualenv exists"
python3 -m venv .venv
echo "Activating virtualenv"
source .venv/bin/activate
echo "Updating python dependencies"
pip3 install --upgrade -r backend/requirements.txt
echo "Updating database"
backend/pact/manage.py migrate
echo "Ensuring default user exists"
cat << EOF | backend/pact/manage.py shell
from django.contrib.auth.models import User

try:
    User.objects.create_superuser('admin', 'admin@example.com', 'pass')
    print('Default user created, username: "admin", password: "pass"')
except Exception:
    pass

EOF

echo "Starting app server"
backend/pact/manage.py runserver 0.0.0.0:8000
