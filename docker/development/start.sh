#!/bin/bash

. /APP/.env
ssh -p 2522 -fN root@$SERVER -L 5432:127.0.0.1:5432
ssh -p 2522 -fN root@$SERVER -L 27017:127.0.0.1:27017
cd /APP/timeseries
gunicorn -c gunicorn_conf.py  app.server:app