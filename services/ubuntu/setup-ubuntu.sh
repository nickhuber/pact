#!/bin/bash
cd /opt/combat_tracker
apt-get update && apt-get install $(cat ubuntu.depends) -y
python3 -m venv .venv
cp services/common/nginx.conf /etc/nginx/conf.d/pact.conf
ln -snf /opt/combat_tracker/services/common/letsencrypt-renew.sh /etc/cron.daily/letsencrypt-renew.sh
systemctl restart nginx
systemctl enable combat_tracker.service
systemctl start combat_tracker.service
