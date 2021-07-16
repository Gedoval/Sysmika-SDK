#!/bin/sh
gunicorn --bind 0.0.0.0:5000 'wsgi:run_app()' -k gevent --worker-connections 1000