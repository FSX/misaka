# -*- coding: utf-8 -*-

import re
import sys
from pathlib import Path
from subprocess import Popen, PIPE

import cffi


MODULE = 'misaka._md4c'

INCLUDE = 'misaka'

HEADERS = (
    'md4c/md4c.h',
    'md4c/render_html.h',
    'md4c/buffer.h',
    'extra.h',
)

SOURCES = (
    'md4c/md4c.c',
    'md4c/entity.c',
    'md4c/render_html.c',
    'md4c/buffer.c',
    'extra.c',
)


RE_FLAG = re.compile(r"""
^\#define
\s+
([A-Z0-9_]+)                      # Flag name.
\s+
(?:
    0 |                           # Zero value.
    0x[A-F0-9]+ |                 # Hexidecimal value.
    \(                            # Flags OR'd together.
        [A-Z0-9_]+
        (?:\s+\|\s+[A-Z0-9_]+)*
    \)
)$
""", flags=re.X)


def in_and_out(args, stdin):
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(stdin)

    if stderr:
        eprint(stderr)
        sys.exit(1)

    stdout = stdout.decode('utf-8')
    return stdout


def merge_headers(headers):
    s = ''

    for h in headers:
        with open(Path(INCLUDE, h), 'r') as fd:
            s += fd.read()

    # Headers are merged so there's no need for local includes.
    # Header contents are also piped through different programs
    # so the preprocessor can't find the includes anyway.
    s = re.sub('#include "[a-zA-Z0-9]+\.h"', '', s)

    return s


def get_flags_from_header(source):
    if isinstance(source, str):
        source = source.encode('utf-8')

    lines = in_and_out(('cpp', '-dM', '-E', '-'), source)

    flags = []

    for line in lines.splitlines():
        if not line.startswith('#define MD_'):
            continue
        match = RE_FLAG.match(line)
        if match is not None:
            # See: https://cffi.readthedocs.io/en/latest/cdef.html?highlight=%23define#letting-the-c-compiler-fill-the-gaps
            flags.append(f'#define {match.group(1)} ...')

    return '\n'.join(flags)


def get_prototypes_from_header(source):
    if isinstance(source, str):
        source = source.encode('utf-8')
    prototypes = in_and_out(('cpp', '-E', '-'), source)
    return prototypes


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


ffi = cffi.FFI()

ffi.set_source(
    MODULE,
    '\n'.join(f'#include "{h}"' for h in HEADERS),
    sources=(str(Path(INCLUDE, s)) for s in SOURCES),
    include_dirs=(INCLUDE,))

header = merge_headers(HEADERS)
proto = get_prototypes_from_header(header)
flags = get_flags_from_header(header)

ffi.cdef(flags)
ffi.cdef(proto)
ffi.compile()
