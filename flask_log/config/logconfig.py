import os
from logging.config import dictConfig

from config import base


def enable():
    log_configuration = base.log_configuration()

    filename = log_configuration.get_optional_property_with_default('filename', 'mylog')
    log_level = log_configuration.get_optional_property_with_default('level', 'DEBUG')
    when = log_configuration.get_optional_property_with_default('when', 'D')
    interval = log_configuration.get_optional_property_with_default('interval', 1)
    backup_count = log_configuration.get_optional_property_with_default('backupCount', 0)
    console_enabled = log_configuration.get_optional_property_with_default('console.enabled', False)
    log_dir = base.add_work_dir_prefix('logs')
    logfile = base.append_path(log_dir, '{0}.log'.format(filename))

    base.make_dir_if_not_exist(log_dir)

    handlers = ['file']
    if console_enabled:
        handlers.append('wsgi')

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }, 'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': logfile,
            'level': log_level,
            'when': when,
            'interval': interval,
            'backupCount': backup_count,
            'formatter': 'default'
        }},
        'root': {
            'level': log_level,
            'handlers': handlers
        }
    })
