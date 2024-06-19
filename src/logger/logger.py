import sys
import logging
from logging.config import dictConfig

logging_config = dict(
    version=1,
    formatters={
        'verbose': {
            'format': ("[%(asctime)s] %(levelname)s "
                       "[%(name)s:%(lineno)s] %(message)s"),
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    handlers={
        'event-logger': {'class': 'logging.handlers.RotatingFileHandler',
                           'formatter': 'verbose',
                           'level': logging.DEBUG,
                           'filename': 'logs/events.log',
                           'maxBytes': 52428800,
                           'backupCount': 7},
        'batch-process-logger': {'class': 'logging.handlers.RotatingFileHandler',
                             'formatter': 'verbose',
                             'level': logging.DEBUG,
                             'filename': 'logs/batch.log',
                             'maxBytes': 52428800,
                             'backupCount': 7},
        'request-logger': {'class': 'logging.handlers.RotatingFileHandler',
                             'formatter': 'verbose',
                             'level': logging.DEBUG,
                             'filename': 'logs/requests.log',
                             'maxBytes': 52428800,
                             'backupCount': 7},
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
    },
    loggers={
        'event_logger': {
            'handlers': ['event-logger', 'console'],
            'level': logging.DEBUG
        },
        'batch_process_logger': {
            'handlers': ['batch-process-logger', 'console'],
            'level': logging.DEBUG
        },
        'request_logger': {
            'handlers': ['request-logger', 'console'],
            'level': logging.DEBUG
        }
    }
)
try:
   dictConfig(logging_config)
except:
   print("Failed to open log file, make sure the /logs directory exists and has the correct permissions")


event_logger = logging.getLogger('event_logger')
batch_process_logger = logging.getLogger('batch_process_logger')
request_logger = logging.getLogger('request_logger')
