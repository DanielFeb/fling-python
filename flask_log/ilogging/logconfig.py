from logging.config import dictConfig

from config import base


def enable():
    log_configuration = base.log_configuration()

    filename = log_configuration.get('fileName', 'mylog')
    log_level = log_configuration.get('level', 'DEBUG')
    when = log_configuration.get('when', 'D')
    interval = log_configuration.get('interval', 1)
    backup_count = log_configuration.get('backupCount', 0)
    console_enabled = log_configuration.get('console.enabled', False)
    log_dir = base.add_work_dir_prefix('logs')
    logfile = base.append_path(log_dir, '{0}.log'.format(filename))

    base.make_dir_if_not_exist(log_dir)

    # on windows, use concurrent-log-handler instead
    handlers = ['concurrent_file']
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
        }, 'concurrent_file': {
            'level': log_level,
            # 如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            # 当达到10MB时分割日志
            'maxBytes': 1024 * 1024 * 10,
            # 最多保留50份文件
            'backupCount': backup_count,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            'filename': logfile,
            'formatter': 'default'
        }},
        'root': {
            'level': log_level,
            'handlers': handlers
        }
    })
