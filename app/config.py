import sys

from dynaconf import Dynaconf
from loguru import logger

settings = Dynaconf(
    envvar_prefix='LAPIG',
    settings_files=[
        'settings.toml',
        '.secrets.toml',
        '../settings.toml',
        '/data/settings.toml',
    ],
    environments=True,
    load_dotenv=True,
)

confi_format = '[ {time} | process: {process.id} | {level: <8}] {module}.{function}:{line} {message}'
rotation = '500 MB'


def start_logger():
    logger.info(f'The system is operating in mode {settings.BRANCH}')


if settings.APP_DEBUG == False:
    logger.remove()
    logger.add(sys.stderr, level='INFO', format=confi_format)

try:
    logger.add(
        '/logs/timeseries/timeseries.log', rotation=rotation, level='INFO'
    )
except:
    logger.add(
        './logs/timeseries/timeseries.log',
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
        './logs/timeseries/timeseries_WARNING.log',
        level='WARNING',
        rotation=rotation,
    )
