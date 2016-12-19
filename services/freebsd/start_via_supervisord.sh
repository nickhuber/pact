#!/usr/bin/env bash

cd /opt/pact

sudo -u pact .venv/bin/pip install -r backend/requirements.txt --upgrade &&
sudo -u pact .venv/bin/python backend/pact/manage.py migrate &&
sudo -u pact .venv/bin/python backend/pact/manage.py collectstatic --clear --noinput &&
sudo -u pact /usr/bin/env bash -c 'cd frontend && npm install' &&
sudo -u pact /usr/bin/env bash -c 'cd frontend && npm update' &&
sudo -u pact /usr/bin/env bash -c 'cd frontend && make' &&
.venv/bin/gunicorn --config gunicorn_config.py pact.wsgi:application
