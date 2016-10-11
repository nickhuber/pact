import grp
import multiprocessing
import os

# TODO: make this better somehow
# Are we www-data (Ubuntu) or www (FreeBSD)
www_group = 'www-data'
for g in grp.getgrall():
    if 'www' in g.gr_name:
        www_group = g.gr_name
        break

bind = 'unix:/opt/pact/.gunicorn.socket'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gaiohttp'
chdir = '/opt/pact/backend/pact'
user = 'pact'
group = www_group
accesslog = '-'
capture_output = True
proc_name = 'PACT'
worker_tmp_dir = '/opt/pact/.tmp'
try:
    os.mkdir(worker_tmp_dir)
except FileExistsError:
    pass
