Misaka
======

.. image:: https://img.shields.io/pypi/v/misaka.svg
    :target: https://pypi.python.org/pypi/misaka

.. image:: https://img.shields.io/pypi/dm/misaka.svg
    :target: https://pypi.python.org/pypi/misaka

.. image:: https://img.shields.io/travis/FSX/misaka.svg
    :target: https://travis-ci.org/FSX/misaka

A CFFI binding for Hoedown_ (version 3), a markdown parsing library.

Documentation can be found at: http://misaka.61924.nl/

.. _Hoedown: https://github.com/hoedown/hoedown


Installation
------------

Misaka has been tested on CPython 2.6, 2.7, 3.2, 3.3, 3.4, 3.5 and PyPy 2.6. It needs
CFFI 1.0 or newer, because of this it will not work on PyPy 2.5 and older.

With pip::

    pip install misaka

Or manually::

    python setup.py install


Example
-------

Very simple example:

.. code:: python

    import misaka as m
    print m.html('some other text')

Or:

.. code:: python

    from misaka import Markdown, HtmlRenderer

    rndr = HtmlRenderer()
    md = Markdown(rndr)

    print(md('some text'))
