from distutils.core import setup, Extension

setup(
    name='pantyshot',
    version='0.1.0',
    ext_modules=[Extension('pantyshot', [
        'pantyshot.c',
        'upskirt/array.c', 'upskirt/buffer.c', 'upskirt/markdown.c', 'upskirt/xhtml.c'
    ])]
)