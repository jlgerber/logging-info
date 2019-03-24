from .context import logging_info, ContextFilter

import unittest
import logging

class TestBasicLoggerPlaceHolderInfo(unittest.TestCase):
    def setUp(self):
        self.placeholder = logging.PlaceHolder('foo')

    def test_init_loggerplaceholderinfo_works(self):
        placeholder_info = logging_info.LoggerPlaceHolderInfo('foo',self.placeholder)
        self.assertEquals(placeholder_info.name, 'foo')


    def test_init_loggerplaceholderinfo_filters_empty(self):
        placeholder_info = logging_info.LoggerPlaceHolderInfo('foo',self.placeholder)
        self.assertEquals(placeholder_info.name, 'foo')
        self.assertEqual(len(placeholder_info.filters),0)
