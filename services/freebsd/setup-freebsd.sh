#!/usr/bin/env bash
cd /opt/pact
pw useradd -n pact -s /bin/false
pw group mod www -m pact
yes | pkg install $(cat freebsd.depends)
python3.5 -m venv .venv
# cp nginx.conf /etc/nginx/conf.d/d20.conf
echo supervisord_enable="YES" > /etc/rc.conf.d/supervisord
echo nginx_enable="YES" > /etc/rc.conf.d/nginx
cp supervisord.conf /usr/local/etc/supervisord.conf
service supervisord restart
service nginx restart
