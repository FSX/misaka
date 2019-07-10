# -*- coding: utf-8 -*-

from ._md4c import lib, ffi
from .constants import PARSER_FLAGS
from .utils import flags_to_int


__all__ = [
    'html',
]


def html(text, parser_flags=None):
    if isinstance(text, str):
        text = text.encode('utf-8')

    parser_flags = flags_to_int(PARSER_FLAGS, parser_flags or tuple())

    b_out = ffi.new('struct membuffer*')
    lib.membuf_init(b_out, int(len(text) * 1.2))

    result = lib.misaka_render_html(text, len(text), b_out, parser_flags, 0)
    assert result == 0

    result = ffi.string(b_out.data, b_out.size).decode('utf-8')

    lib.membuf_fini(b_out)

    return result
