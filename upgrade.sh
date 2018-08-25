#!/bin/bash

/opt/pact/.venv/bin/pip install -r /opt/pact/backend/requirements.txt --upgrade
/opt/pact/.venv/bin/python /opt/pact/backend/pact/manage.py migrate
/opt/pact/.venv/bin/python /opt/pact/backend/pact/manage.py collectstatic --clear --noinput

pushd /opt/pact/frontend/
    npm install
    npm update
    make
popd
