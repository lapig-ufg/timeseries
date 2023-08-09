#!/bin/bash

cd /APP/download-minio
gunicorn -c gunicorn_conf.py  app.server:app"