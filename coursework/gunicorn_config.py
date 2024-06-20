command = '/home/www/course_work/env/bin/gunicorn'
pythonpath = '/home/www/course_work'
bind = '127.0.0.1:8001'
workers = 3
user = 'root'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=coursework.settings'
