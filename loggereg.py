import logging,logging.config

from logging_eg import customfilter
from logging_eg import constants
import os

LOGGING = {
        'version': 1,
        'filters': {
            'ddfilter': {
                '()': customfilter.DdFilter,
            }
        },
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
            },
            'dd': {
                'class': 'logging.Formatter',
                'format': constants.DD_FORMAT
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'dd',
                'filters': ['ddfilter']
            },
            'ddconsole': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'dd',
                'filters': ['ddfilter']
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'mplog.log',
                'mode': 'w',
                'formatter': 'detailed',
            },
            'ddfile': {
                'class': 'logging.FileHandler',
                'filename': 'mplog.log',
                'mode': 'w',
                'formatter': 'dd',
                'filters': ['ddfilter']
            },
            'errors': {
                'class': 'logging.FileHandler',
                'filename': 'mplog-errors.log',
                'mode': 'w',
                'level': 'ERROR',
                'formatter': 'detailed',
            },
        },
        'loggers': {
            'dd': {
                'level': 'DEBUG',
                'propagate': False,
                'handlers': ['ddfile', 'ddconsole']
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }
logging.config.dictConfig(LOGGING)

def doit():
    os.environ['DD_SHOW'] = "SRGTBILKO"
    os.environ["DD_USER"] = "clu"
    os.environ["DD_OS"] = "cent7_64"

    root_log = logging.getLogger()
    dd_log = logging.getLogger("dd."+ __name__)

    root_log.debug("a root debug message")
    dd_log.debug("a dd debug message")

    root_log.info("a root info message")
    dd_log.info("a dd info message")

    root_log.warn("a root warn message")
    dd_log.warn("a dd warn message")


if __name__ == "__main__":
    doit()