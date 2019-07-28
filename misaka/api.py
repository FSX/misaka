from dataclasses import dataclass, field as dataclass_field, fields as dataclass_fields
from enum import IntEnum

from . import const
from . import callbacks  # Activate CFFI callbacks.
from ._md4c import lib, ffi
from .utils import flags_to_int, Buffer


__all__ = [
    'html',
    'Base',
]


EMPTY = tuple()


# TODO: Render flags.
def html(text, parser_flags=None):
    if isinstance(text, str):
        text = text.encode('utf-8')

    parser_flags = flags_to_int(const.PARSER_FLAGS, parser_flags or EMPTY)

    b_out = _new_buffer(int(len(text) * 1.2))

    status = lib.misaka_render_html(text, len(text), b_out, parser_flags, 0)
    _check_status(status, 'misaka_render_html()')

    result = _buffer_to_str(b_out)
    _free_buffer(b_out)

    return result


class Base:
    def __init__(self, parser_flags=None):
        parser_flags = flags_to_int(const.PARSER_FLAGS, parser_flags or EMPTY)

        self.parser = ffi.new('MD_PARSER *')
        self.parser.abi_version = 0
        self.parser.flags = parser_flags
        self.parser.enter_block = lib._misaka_enter_block
        self.parser.leave_block = lib._misaka_leave_block
        self.parser.enter_span = lib._misaka_enter_span
        self.parser.leave_span = lib._misaka_leave_span
        self.parser.text = lib._misaka_text
        self.parser.debug_log = lib._misaka_debug_log
        self.parser.syntax = ffi.NULL

    def render(self, text):
        if isinstance(text, str):
            text = text.encode('utf-8')

        try:
            obuffer = Buffer(self.approximate_buffer_size(text))
            session = _Session(self, obuffer)
            handle = ffi.new_handle(session)
            status = lib.md_parse(text, len(text), self.parser, handle)

            _check_status(status, 'md_parse()')

            result = obuffer.to_str()
            return result
        finally:
            obuffer.fini()

    __call__ = render

    def approximate_buffer_size(self, text):
        return int(len(text) * 1.2)

    def enter_block(self, out, type, detail):
        raise NotImplementedError

    def leave_block(self, out, type, detail):
        raise NotImplementedError

    def enter_span(self, out, type, detail):
        raise NotImplementedError

    def leave_span(self, out, type, detail):
        raise NotImplementedError

    def text(self, out, type, text):
        raise NotImplementedError

    def debug(self, msg):
        raise NotImplementedError


class _Session:
    __slots__ = ('renderer', 'buffer')

    def __init__(self, renderer, buffer):
        self.renderer = renderer
        self.buffer = buffer


def _check_status(status, func_name):
    if status == -1:
        raise MemoryError(f'{func_name} ran out of memory')
    if status > 0:
        raise RuntimeError(f'{func_name} exited with status code {status}')
