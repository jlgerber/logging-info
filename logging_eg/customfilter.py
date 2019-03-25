import logging
import os

from .constants import *

class DdFilter(logging.Filter):
    """
    Custom filter test
    """
    def filter(self, record):
        record.dd_level = self._get_level()
        record.dd_user = os.environ.get("DD_USER")
        record.dd_os = os.environ.get("DD_OS")
        return True

    def _get_level(self):
        return ".".join(filter(None,[os.environ.get(x) for x in ("DD_SHOW", "DD_SEQ", "DD_SHOT")]))


