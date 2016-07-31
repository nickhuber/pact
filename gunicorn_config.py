import multiprocessing

bind = 'unix:/opt/combat_tracker/.gunicorn.socket'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gaiohttp'
chdir = '/opt/combat_tracker/backend/combat_tracker'
user = 'combat_tracker'
group = 'combat_tracker'
accesslog = '-'
capture_output = True
proc_name = 'Combat Tracker'
