# -*- coding: utf-8 -*-

from chibitest import TestCase, ok
from misaka import extension_map, \
    EXT_TABLES, EXT_FENCED_CODE, EXT_FOOTNOTES
from misaka.utils import args_to_int


class ArgsToIntTest(TestCase):
    def test_args(self):
        expected = EXT_TABLES | EXT_FENCED_CODE | EXT_FOOTNOTES
        result = args_to_int(
            extension_map,
            ('tables', 'fenced-code', 'footnotes'))

        ok(result) == expected

    def test_int(self):
        expected = EXT_TABLES | EXT_FENCED_CODE | EXT_FOOTNOTES
        result = args_to_int(extension_map, expected)

        ok(result) == expected
