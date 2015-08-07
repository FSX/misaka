# -*- coding: utf-8 -*-

from chibitest import TestCase, ok
from misaka import reduce_dict, extension_map, \
    EXT_TABLES, EXT_FENCED_CODE, EXT_FOOTNOTES


class ReduceDictTest(TestCase):
    def test_from_dict(self):
        expected = EXT_TABLES | EXT_FENCED_CODE | EXT_FOOTNOTES
        result = reduce_dict(
            extension_map,
            ('tables', 'fenced-code', 'footnotes'))

        ok(result) == expected

    def test_from_int(self):
        expected = EXT_TABLES | EXT_FENCED_CODE | EXT_FOOTNOTES
        result = reduce_dict(extension_map, expected)

        ok(result) == expected
