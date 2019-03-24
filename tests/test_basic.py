
from .context import logging_info

import unittest
import logging

class TestBasic(unittest.TestCase):
    def setUp(self):
        logging.basicConfig()
        self.root_logger = logging.getLogger()
        self.foo_logger = logging.getLogger('foo')
        self.bar_logger = logging.getLogger('bar')

    def test_logInfo_basic_init_works(self):
        lh = logging_info.LoggerInfo('foo', self.foo_logger)
        self.assertEqual(lh.level,0)
        self.assertEquals(self.foo_logger.name, "foo")
        self.assertEqual(self.foo_logger.handlers, [])
        self.assertEqual(self.foo_logger.filters, [])

    def test_logInfo_corectly_reports_set_level(self):
        self.foo_logger.level = 20
        lh = logging_info.LoggerInfo('foo', self.foo_logger)
        self.assertEqual(lh.level,20)
        self.assertEquals(self.foo_logger.name, "foo")
        self.assertEqual(self.foo_logger.handlers, [])
        self.assertEqual(self.foo_logger.filters, [])

    def test_logInfo_corectly_reports_set_level(self):
        lh = logging_info.LoggerInfo('foo', self.foo_logger)
        self.assertEqual(lh.level,0)
        self.assertEquals(self.foo_logger.name, "foo")
        self.assertEqual(self.foo_logger.handlers, [])
        self.assertEqual(self.foo_logger.filters, [])

    def test_logInfo_corectly_reports_set_handler(self):
        try:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            self.foo_logger.addHandler(ch)
            lh = logging_info.LoggerInfo('foo', self.foo_logger)
            self.assertEqual(lh.level,0)
            self.assertEquals(self.foo_logger.name, "foo")
            self.assertEqual(len(self.foo_logger.handlers), 1)
            self.assertEqual(self.foo_logger.handlers[0], ch)
            self.assertEqual(self.foo_logger.filters, [])
        finally:
            self.foo_logger.removeHandler(ch)

    def test_logInfo_corectly_reports_set_filter(self):

        class ContextFilter(logging.Filter):
            """
            test filter from python documentation
            """
            USERS = ['jim', 'fred', 'sheila']
            IPS = ['123.231.231.123', '127.0.0.1', '192.168.0.1']
            def filter(self, record):
                record.ip = choice(ContextFilter.IPS)
                record.user = choice(ContextFilter.USERS)
                return True
        try:
            fltr = ContextFilter()
            self.foo_logger.addFilter(fltr)
            lh = logging_info.LoggerInfo('foo', self.foo_logger)
            self.assertEqual(lh.level,0)
            self.assertEquals(self.foo_logger.name, "foo")
            self.assertEqual(self.foo_logger.handlers, [])
            self.assertEqual(len(self.foo_logger.filters), 1)
            self.assertEqual(self.foo_logger.filters[0], fltr)
        finally:
            self.foo_logger.removeFilter(fltr)

