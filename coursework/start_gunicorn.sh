#!/bin/bash
source /home/www/course_work/env/bin/activate
exec gunicorn -c "/home/www/course_work/gunicorn_config.py" coursework.wsgi
