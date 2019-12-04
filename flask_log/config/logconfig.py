import os
from logging.config import dictConfig


def make_dir(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)


def enable():
    filedir = os.path.abspath(os.path.dirname(__file__))
    basedir = os.path.abspath(os.path.dirname(filedir))
    logdir = "{0}/logs/".format(basedir)
    logfile = "{0}flask.log".format(logdir)

    make_dir(logdir)

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
            'level': 'DEBUG',
            'when': 'M',
            'interval': 1,
            'backupCount': 0,
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi', 'file']
        }
    })
