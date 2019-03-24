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
        self.assertEqual(len(placeholder_info.filters),0)

    def test_init_loggerplaceholderinfo_handlers_empty(self):
        placeholder_info = logging_info.LoggerPlaceHolderInfo('foo',self.placeholder)
        self.assertEqual(len(placeholder_info.handlers),0)

    def test_init_loggerplaceholderinfo_cannot_mutate_handlers(self):
        placeholder_info = logging_info.LoggerPlaceHolderInfo('foo',self.placeholder)
        self.assertEqual(len(placeholder_info.handlers), 0)
        with self.assertRaises(AttributeError) as context:
            placeholder_info.handlers = ['foo']
        self.assertTrue("can't set attribute" in context.exception)
        with self.assertRaises(AttributeError) as context:
            placeholder_info.handlers.append("foo")
        self.assertTrue("'frozenset' object has no attribute 'append'")

    def test_init_loggerplaceholderinfo_cannot_mutate_filters(self):
        placeholder_info = logging_info.LoggerPlaceHolderInfo('foo',self.placeholder)
        self.assertEqual(len(placeholder_info.handlers), 0)
        with self.assertRaises(AttributeError) as context:
            placeholder_info.filters = ['foo']
        self.assertTrue("can't set attribute" in context.exception)
        with self.assertRaises(AttributeError) as context:
            placeholder_info.filters.append("foo")
        self.assertTrue("'frozenset' object has no attribute 'append'")