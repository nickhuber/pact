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

bind = 'unix:/opt/combat_tracker/.gunicorn.socket'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gaiohttp'
chdir = '/opt/combat_tracker/backend/combat_tracker'
user = 'combat_tracker'
group = www_group
accesslog = '-'
capture_output = True
proc_name = 'Combat Tracker'
worker_tmp_dir = '/opt/combat_tracker/.tmp'
try:
    os.mkdir(worker_tmp_dir)
except FileExistsError:
    pass
