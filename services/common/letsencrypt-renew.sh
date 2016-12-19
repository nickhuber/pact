#!/bin/bash

letsencrypt --renew --config /opt/pact/services/common/letsencrypt.conf certonly

systemctl restart nginx
