#!/bin/bash

cd /APP/timeseries
gunicorn -c gunicorn_conf.py  app.server:app