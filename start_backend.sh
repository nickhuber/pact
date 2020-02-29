#!/usr/bin/env bash

set -e

if [ "$(whoami)" != "pact" ]; then
    echo "Script must be run as user: pact"
    exit -1
fi

echo "Ensuring virtualenv exists"
test ! -d .venv && python3 -m venv .venv

echo "Updating python dependencies"
.venv/bin/pip3 install wheel
.venv/bin/pip3 install --upgrade -r backend/requirements.txt

echo "Updating database"
.venv/bin/python3 backend/pact/manage.py migrate

echo "Ensuring default user exists"
cat << EOF | .venv/bin/python3 backend/pact/manage.py shell
from django.contrib.auth.models import User

try:
    User.objects.create_superuser('admin', 'admin@example.com', 'pass')
    print('Default user created, username: "admin", password: "pass"')
except Exception:
    pass

EOF

echo "Starting app server"
.venv/bin/python3 backend/pact/manage.py runserver 0.0.0.0:8000
