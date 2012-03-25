.. _installation:

Installation
============

Misaka supports Python 2 and 3 (tested with 2.7 and 3.2). Misaka can be
installed with *easy_install* or pip_::

    pip install misaka

The latest sources can be cloned from the `Github repository`_ and
installed with::

   python setup.py install

Cython_ is only needed when you would like to regenerate the C file(s). This
can be done by using the ``--cython`` option. For example::

   python setup.py install --cython


.. _Cython: http://cython.org/
.. _pip: http://www.pip-installer.org/
.. _Github repository: https://github.com/FSX/misaka


Visual Studio
-------------

Visual Studio's support for C is not optimal and most VS compilers are missing
``stdint.h``, which is needed to compile Misaka. This file can be downloaded
from msinttypes_ and put into ``C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\include``
for example.


.. _msinttypes: http://msinttypes.googlecode.com/svn/trunk/stdint.h
