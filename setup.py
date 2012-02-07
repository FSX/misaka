import sys

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension


if sys.argv[-1] == '--cython':
    sys.argv.remove('--cython')
    try:
        from Cython.Compiler.Main import compile
        compile('src/misaka.pyx')
    except ImportError:
        print('Cython is not installed. Please install Cython first.')
        sys.exit()


setup(
    name='misaka',
    version='1.0.1',
    description='The Python binding for Sundown, a markdown parsing library.',
    author='Frank Smit',
    author_email='frank@61924.nl',
    url='http://misaka.61924.nl/',
    license='MIT',
    long_description=open('README.rst').read(),
    ext_modules=[Extension('misaka', [
        'src/misaka.c',
        'src/wrapper.c',
        'src/sundown/stack.c',
        'src/sundown/buffer.c',
        'src/sundown/markdown.c',
        'src/sundown/html.c',
        'src/sundown/html_smartypants.c',
        'src/sundown/houdini_href_e.c',
        'src/sundown/houdini_html_e.c',
        'src/sundown/autolink.c'
    ])],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities'
    ]
)
