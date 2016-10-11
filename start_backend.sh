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
echo "Starting app server"
backend/pact/manage.py runserver 0.0.0.0:8000
