import os
import os.path
import shutil
import subprocess
import sys
from setuptools import setup, Command


install_requires=['cffi>=1.0.0']
try:
    import importlib
except ImportError:
    install_requires.append('importlib')

dirname = os.path.dirname(os.path.abspath(__file__))


class TestCommand(Command):
    description = 'run tests'
    user_options = [
        ('include=', 'i', 'comma separated list of testcases'),
        ('exclude=', 'e', 'comma separated list of testcases'),
        ('benchmark', 'b', 'run bechmarks'),
        ('list', 'l', 'list all testcases'),
    ]

    def initialize_options(self):
        self.include = ''
        self.exclude = ''
        self.benchmark = 0
        self.list = 0

    def finalize_options(self):
        pass

    def run(self):
        self.run_command('develop')
        errno = subprocess.call([sys.executable, 'tests/run_tests.py'] + sys.argv[2:])
        sys.exit(errno)


setup(
    name='misaka',
    version='2.1.0',
    description='A CFFI binding for Hoedown, a markdown parsing library.',
    author='Frank Smit',
    author_email='frank@61924.nl',
    url='https://github.com/FSX/misaka',
    license='MIT',
    long_description=open(os.path.join(dirname, 'README.rst')).read(),
    scripts=['scripts/misaka'],
    packages=['misaka'],
    cmdclass={
        'test': TestCommand
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities'
    ],
    setup_requires=['cffi>=1.0.0'],
    install_requires=install_requires,
    cffi_modules=['build_ffi.py:ffi'],
)
