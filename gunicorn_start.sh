#!/usr/bin/env bash

cd /home/jileon/workarea/euribates/matraka
source /home/jileon/.pyenv/versions/matraka/bin/activate
python -m gunicorn main.wsgi:application --workers 2 --reload --bind 0.0.0.0:8002
