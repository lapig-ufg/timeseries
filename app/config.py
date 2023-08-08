import os
import sys

from dynaconf import Dynaconf
from loguru import logger


def start_logger():
    type_logger = 'development'
    if os.environ.get('APP_DEBUG') == True:
        type_logger = 'production'
    logger.info(f'The system is operating in mode {type_logger}')


confi_format = '[ {time} | process: {process.id} | {level: <8}] {module}.{function}:{line} {message}'
rotation = '500 MB'


if os.environ.get('APP_DEBUG') == True:
    logger.remove()
    logger.add(sys.stderr, level='INFO', format=confi_format)

try:
    logger.add(
        '/logs/timeseries/timeseries.log', rotation=rotation, level='INFO'
    )
except:
    logger.add(
        '../logs/timeseries/timeseries.log',
        rotation=rotation,
        level='INFO',
    )
try:
    logger.add(
        '/logs/timeseries/timeseries_WARNING.log',
        level='WARNING',
        rotation=rotation,
    )
except:
    logger.add(
        '../logs/timeseries/timeseries_WARNING.log',
        level='WARNING',
        rotation=rotation,
    )

settings = Dynaconf(
    envvar_prefix='MINIO',
    settings_files=[
        'settings.toml',
        '.secrets.toml',
        '../settings.toml',
        '/data/settings.toml',
    ],
    environments=True,
    load_dotenv=True,
)