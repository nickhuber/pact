#!/bin/bash
set -e

cd /opt/pact

# Dependencies
dnf install $(cat linux.depends) -y

# Frontend stuff
pushd frontend
    npm install
    npm build
popd

# Backend stuff
python3 -m venv .venv

# Service management
cp services/common/nginx.conf /etc/nginx/conf.d/pact.conf
ln -snf /opt/pact/services/common/letsencrypt-renew /etc/cron.daily/letsencrypt-renew.sh
useradd pact
chown -R pact:pact /opt/pact
systemctl enable pact.socket
systemctl start pact.socket
systemctl restart nginx
