from distutils.core import setup, Extension

setup(
    name='pantyshot',
    version='0.1.0',
    description='Python extension for Upskirt.',
    author='Frank Smit',
    author_email='frank@61924.nl',
    url='https://github.com/FSX/pantyshot',
    ext_modules=[Extension('pantyshot', [
        'src/pantyshot.c',
        'src/upskirt/array.c',
        'src/upskirt/buffer.c',
        'src/upskirt/markdown.c',
        'src/upskirt/xhtml.c'
    ])]
)