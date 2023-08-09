from multiprocessing import cpu_count
from app.config import settings

# Socket Path

#bind = 'unix:./gunicorn.sock'
bind = f'{settings.HOST}:{settings.PORT}'

# Worker Options
workers = int(cpu_count() / 2)
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
timeout = 0
host = settings.HOST
port = settings.PORT
if settings.APP_DEBUG == True:
    loglevel = 'debug'
else:
    loglevel = 'info'
accesslog = './logs/access.log'
errorlog = './logs/error.log'
reload=settings.APP_DEBUG
log_config=settings.LOG_CONFIG



