import os.path
from setuptools import setup


install_requires=['cffi>=1.0.0']
try:
    import importlib
except ImportError:
    install_requires.append('importlib')

dirname = os.path.dirname(os.path.abspath(__file__))


setup(
    name='misaka',
    version='3.0.0',
    description='A CFFI binding for MD4C, a markdown parsing library.',
    author='Frank Smit',
    author_email='frank@61924.nl',
    url='https://github.com/FSX/misaka',
    license='MIT',
    long_description=open(os.path.join(dirname, 'README.rst')).read(),
    packages=['misaka'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: C',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
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
