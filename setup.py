from distutils.core import setup, Extension

setup(
    name='pantyshot',
    version='0.3.0',
    description='A Python binding for Upskirt.',
    author='Frank Smit',
    author_email='frank@61924.nl',
    url='http://pantyshot.61924.nl/',
    license='MIT',
    long_description=open('README.txt').read(),
    ext_modules=[Extension('pantyshot', [
        'src/pantyshot.c',
        'src/upskirt/array.c',
        'src/upskirt/buffer.c',
        'src/upskirt/markdown.c',
        'src/upskirt/html.c',
        'src/upskirt/html_smartypants.c',
        'src/upskirt/autolink.c',
        'src/upskirt/html_autolink.c'
    ])]
)
