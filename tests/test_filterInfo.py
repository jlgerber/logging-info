from .context import logging_info, ContextFilter

import unittest
import logging

class TestBasicFilterInfo(unittest.TestCase):
    def setUp(self):
        self.context_filter = ContextFilter()

    def test_filterInfo_class_set(self):
        cfi = logging_info.FilterInfo(self.context_filter)
        self.assertEquals(cfi.class_name, "ContextFilter")