import grp
import multiprocessing
import os

# TODO: make this better somehow
# Are we nginx (Fedora) or www (FreeBSD)
web_group = 'nginx'
for g in grp.getgrall():
    if 'www' in g.gr_name:
        web_group = g.gr_name
        break

bind = 'unix:/run/pact-gunicorn.socket'
workers = multiprocessing.cpu_count() * 2 + 1
chdir = '/opt/pact/backend/pact'
user = 'pact'
group = web_group
accesslog = '-'
capture_output = True
proc_name = 'PACT'
worker_tmp_dir = '/opt/pact/.tmp'
try:
    os.mkdir(worker_tmp_dir)
except FileExistsError:
    pass
