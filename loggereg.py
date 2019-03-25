import logging,logging.config

from logging_eg import customfilter
from logging_eg import constants
import os

LOGGING = {
        'version': 1,
        'filters': {
            'adfilter': {
                '()': customfilter.AdFilter,
            }
        },
        'formatters': {
            'detailed': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
            },
            'ad': {
                'class': 'logging.Formatter',
                'format': constants.AD_FORMAT
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'ad',
                'filters': ['adfilter']
            },
            'adconsole': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'ad',
                'filters': ['adfilter']
            },
            'file': {
                'class': 'logging.FileHandler',
                'filename': 'mplog.log',
                'mode': 'w',
                'formatter': 'detailed',
            },
            'adfile': {
                'class': 'logging.FileHandler',
                'filename': 'mplog.log',
                'mode': 'w',
                'formatter': 'ad',
                'filters': ['adfilter']
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
            'ad': {
                'level': 'DEBUG',
                'propagate': False,
                'handlers': ['adfile', 'adconsole']
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }
logging.config.dictConfig(LOGGING)

def doit():
    os.environ['AD_SHOW'] = "SRGTBILKO"
    os.environ["AD_USER"] = "clu"
    os.environ["AD_OS"] = "cent7_64"

    root_log = logging.getLogger()
    ad_log = logging.getLogger("ad."+ __name__)

    root_log.debug("a root debug message")
    ad_log.debug("a ad debug message")

    root_log.info("a root info message")
    ad_log.info("a ad info message")

    root_log.warn("a root warn message")
    ad_log.warn("a ad warn message")


if __name__ == "__main__":
    doit()