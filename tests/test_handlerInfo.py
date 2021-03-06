from .context import logging_info, ContextFilter

import unittest
import logging


class TestBasicHandlerInfo(unittest.TestCase):
    def setUp(self):
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.DEBUG)

    def test_handlerInfo_basic_init_works(self):
        handler = logging_info.HandlerInfo(self.stream_handler)
        self.assertEquals(handler.name, None)
        self.assertEquals(handler.class_name, "StreamHandler")
        self.assertEqual(handler.level, 10)
        self.assertEqual([x for x in handler.filters], [])
        self.assertEqual(handler.filter_cnt, 0)

    def test_handlerInfo_set_name_recognized(self):
        try:
            self.stream_handler.set_name('stream')
            handler = logging_info.HandlerInfo(self.stream_handler)
            self.assertEquals(handler.name, "stream")
            self.assertEquals(handler.class_name, "StreamHandler")
            self.assertEqual(handler.level, 10)
            self.assertEqual([x for x in handler.filters], [])
            self.assertEqual(handler.filter_cnt, 0)
        finally:
            self.stream_handler.set_name(None)

    def test_handlerInfo_filters_recognized(self):
        try:
            fltr = ContextFilter()
            self.stream_handler.addFilter(fltr)
            handler = logging_info.HandlerInfo(self.stream_handler)
            self.assertEquals(handler.name, None)
            self.assertEquals(handler.class_name, "StreamHandler")
            self.assertEqual(handler.level, 10)
            self.assertEqual(len([x for x in handler.filters]), 1)
            self.assertEqual(handler.filter_cnt, 1)
            self.assertEqual(next(handler.filters).__class__.__name__, "FilterInfo")
        finally:
            self.stream_handler.removeFilter(fltr)