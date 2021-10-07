import multiprocessing

bind = '0.0.0.0:8000'
chdir = '/app'
accesslog = '-'
capture_output = True
proc_name = 'PACT'
chdir = 'pact'
workers = multiprocessing.cpu_count() * 2 + 1
