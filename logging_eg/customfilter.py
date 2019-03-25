import logging
import os

from .constants import *

class AdFilter(logging.Filter):
    """
    Custom filter test for a ficticious VFX company called Analog Domain, or AD
    """
    def filter(self, record):
        record.ad_level = self._get_level()
        record.ad_user = os.environ.get("AD_USER")
        record.ad_os = os.environ.get("AD_OS")
        return True

    def _get_level(self):
        return ".".join(filter(None,[os.environ.get(x) for x in ("AD_SHOW", "AD_SEQ", "AD_SHOT")]))


