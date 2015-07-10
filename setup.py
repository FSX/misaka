import os
import os.path
import shutil
import subprocess
import sys
from setuptools import setup, Command


dirname = os.path.dirname(os.path.abspath(__file__))


class BaseCommand(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass


class CleanCommand(BaseCommand):
    description = 'cleanup directories created by packaging and build processes'
    def run(self):
        for path in ('build', 'dist', 'misaka.egg-info', 'docs/_build'):
            if os.path.exists(path):
                path = os.path.join(dirname, path)
                print('removing %s' % path)
                shutil.rmtree(path)


class TestCommand(BaseCommand):
    description = 'run unit tests'
    def run(self):
        errno = subprocess.call([sys.executable, 'tests/runner.py'])
        sys.exit(errno)


setup(
    name='misaka',
    version='2.0.0',
    description='A CFFI binding for Hoedown, a markdown parsing library.',
    author='Frank Smit',
    author_email='frank@61924.nl',
    url='https://github.com/FSX/misaka',
    license='MIT',
    long_description=open(os.path.join(dirname, 'README.rst')).read(),
    scripts=['scripts/misaka'],
    cmdclass={
        'clean': CleanCommand,
        'test': TestCommand
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities'
    ],
    setup_requires=['cffi>=1.0.0'],
    install_requires=['cffi>=1.0.0'],
    cffi_modules=['build_ffi.py:ffi'],
)
