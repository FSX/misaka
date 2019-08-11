import sys
from inspect import getmembers

from ._md4c import lib


def _set_constants(target_mapping, match_prefix, strip_prefix):
    is_int = lambda n: isinstance(n, int)

    for name, value in getmembers(lib, is_int):
        if not name.startswith(match_prefix):
            continue
        name = name[len(strip_prefix):]
        setattr(sys.modules[__name__], name, value)
        target_mapping[name.lower()] = value


PARSER_FLAGS = {}
BLOCK_TYPE = {}
SPAN_TYPE = {}
TEXT_TYPE = {}
ALIGN = {}


if not hasattr(sys.modules[__name__], 'MD_FLAG_TASKLISTS'):
    _set_constants(PARSER_FLAGS, 'MD_FLAG_', 'MD_FLAG_')
    _set_constants(BLOCK_TYPE, 'MD_BLOCK_', 'MD_')
    _set_constants(SPAN_TYPE, 'MD_SPAN_', 'MD_')
    _set_constants(TEXT_TYPE, 'MD_TEXT_', 'MD_')
    _set_constants(ALIGN, 'MD_ALIGN_', 'MD_ALIGN_')
