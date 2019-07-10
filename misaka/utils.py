# -*- coding: utf-8 -*-


def flags_to_int(mapping, flags):
    if not isinstance(flags, (tuple, list)):
        raise TypeError('flags must be a tuple or list')

    value = 0
    for v in flags:
        value |= v

    return value
