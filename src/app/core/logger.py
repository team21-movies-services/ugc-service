from .config import settings

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT,
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': settings.project.log_level,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': settings.project.log_level,
        },
        'gunicorn.error': {
            'level': settings.project.log_level,
        },
        'gunicorn.access': {
            'handlers': ['access'],
            'level': settings.project.log_level,
            'propagate': False,
        },
    },
    'root': {
        'level': settings.project.log_level,
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
