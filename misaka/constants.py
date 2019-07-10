# -*- coding: utf-8 -*-

import sys
from inspect import getmembers

from ._md4c import lib


def _set_constants(target_mapping, prefix):
    is_int = lambda n: isinstance(n, int)

    for name, value in getmembers(lib, is_int):
        if not name.startswith(prefix):
            continue
        setattr(sys.modules[__name__], name, value)
        target_mapping[name[len(prefix):].lower()] = value


PARSER_FLAGS = {}


if not hasattr(sys.modules[__name__], 'MD_FLAG_TASKLISTS'):
    _set_constants(PARSER_FLAGS, 'MD_FLAG_')
