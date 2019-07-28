from ._md4c import ffi, lib


def flags_to_int(mapping, flags):
    if not isinstance(flags, (tuple, list)):
        raise TypeError('flags must be a tuple or list')

    value = 0
    for v in flags:
        value |= mapping[v]

    return value


def buffer_to_string(buffer):
    if buffer == ffi.NULL or buffer.size == 0:
        return ''
    return cstr_to_str(buffer.data, buffer.size)


def cstr_to_str(text, size=-1):
    return ffi.string(text, size).decode('utf-8', 'ignore')


class Buffer:
    def __init__(self, size):
        self._storage = ffi.new('struct membuffer *')
        lib.membuf_init(self._storage, size)

    def to_str(self):
        return buffer_to_string(self._storage)

    def fini(self):
        lib.membuf_fini(self._storage)

    def append(self, text):
        if isinstance(text, str):
            text = text.encode('utf-8')
        lib.membuf_append(self._storage, text, len(text))
