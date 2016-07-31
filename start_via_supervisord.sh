#!/usr/bin/env bash

cd /opt/combat_tracker
sudo -u combat_tracker .venv/bin/pip install -r backend/requirements.txt --upgrade &&
sudo -u combat_tracker .venv/bin/python backend/combat_tracker/manage.py migrate &&
sudo -u combat_tracker .venv/bin/python backend/combat_tracker/manage.py collectstatic --clear --noinput &&
sudo -u combat_tracker /usr/bin/env bash -c 'cd frontend && npm install' &&
sudo -u combat_tracker /usr/bin/env bash -c 'cd frontend && npm update' &&
sudo -u combat_tracker /usr/bin/env bash -c 'cd frontend && ./node_modules/.bin/bower install' &&
sudo -u combat_tracker /usr/bin/env bash -c 'cd frontend && npm run grunt' &&
.venv/bin/gunicorn --config gunicorn_config.py combat_tracker.wsgi:application
