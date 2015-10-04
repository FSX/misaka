# -*- coding: utf-8 -*-

from chibitest import TestCase, ok
from misaka import _args_to_int, extension_map, \
    EXT_TABLES, EXT_FENCED_CODE, EXT_FOOTNOTES


class ArgsToIntTest(TestCase):
    def test_args(self):
        expected = EXT_TABLES | EXT_FENCED_CODE | EXT_FOOTNOTES
        result = _args_to_int(
            extension_map,
            ('tables', 'fenced-code', 'footnotes'))

        ok(result) == expected

    def test_int(self):
        expected = EXT_TABLES | EXT_FENCED_CODE | EXT_FOOTNOTES
        result = _args_to_int(extension_map, expected)

        ok(result) == expected
