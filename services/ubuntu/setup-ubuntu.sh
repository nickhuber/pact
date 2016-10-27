#!/bin/bash
cd /opt/pact
apt-get update && apt-get install $(cat ubuntu.depends) -y
gem install sass
python3 -m venv .venv
cp services/common/nginx.conf /etc/nginx/conf.d/pact.conf
ln -snf /opt/pact/services/common/letsencrypt-renew.sh /etc/cron.daily/letsencrypt-renew.sh
useradd pact
chown -R pact:pact /opt/pact
systemctl restart nginx
systemctl enable pact.service
systemctl start pact.service
