#!/bin/bash
cd /opt/pact
dnf install $(cat linux.depends) -y
python3 -m venv .venv
cp services/common/nginx.conf /etc/nginx/conf.d/pact.conf
ln -snf /opt/pact/services/common/letsencrypt-renew /etc/cron.daily/letsencrypt-renew.sh
useradd pact
chown -R pact:pact /opt/pact
systemctl enable pact.socket
systemctl start pact.socket
systemctl restart nginx
