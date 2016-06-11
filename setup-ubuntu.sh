#!/bin/bash
apt-get update && apt-get install $(cat ubuntu.depends) -y
python3 -m venv .venv
cp nginx.conf /etc/nginx/conf.d/d20.conf
systemctl restart nginx
systemctl enable combat_tracker.service
systemctl start combat_tracker.service
