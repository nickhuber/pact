#!/bin/bash

letsencrypt --renew --config /opt/combat_tracker/services/common/letsencrypt.conf certonly

systemctl restart nginx
