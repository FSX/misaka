import sys
from setuptools import Extension, setup

try:
    from Cython.Distutils import build_ext
except ImportError:
    print('Cython is not installed. Please install Cython first.')
    sys.exit()


setup(
    name='misaka',
    version='1.0.0',
    description='The Python binding for Sundown, a markdown parsing library.',
    author='Frank Smit',
    author_email='frank@61924.nl',
    url='http://misaka.61924.nl/',
    license='MIT',
    long_description=open('README.rst').read(),
    install_requires=['cython'],
    cmdclass = {'build_ext': build_ext},
    ext_modules=[Extension('misaka', [
        'src/misaka.pyx',
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
