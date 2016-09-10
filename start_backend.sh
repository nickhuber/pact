#!/usr/bin/env bash

echo "Ensuring virtualenv exists"
python3 -m venv .venv
echo "Activating virtualenv"
source .venv/bin/activate
echo "Updating python dependencies"
pip3 install --upgrade -r backend/requirements.txt
echo "Updating database"
backend/combat_tracker/manage.py migrate
echo "Starting app server"
backend/combat_tracker/manage.py runserver 0.0.0.0:8000
