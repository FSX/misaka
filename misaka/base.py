from . import const
from . import callbacks  # Activate CFFI callbacks.
from ._md4c import lib, ffi
from .utils import check_status, flags_to_int, Buffer


__all__ = [
    'Base',
]


EMPTY = tuple()


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

        with Buffer(self.approximate_buffer_size(text)) as ob:
            session = _Session(self, ob)
            handle = ffi.new_handle(session)
            status = lib.md_parse(text, len(text), self.parser, handle)

            check_status(status, 'md_parse()')

            result = ob.to_str()
            return result

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
