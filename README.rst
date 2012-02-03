Misaka
======

The Python binding for Sundown_, a markdown parsing library.

Documentation can be found at: http://misaka.61924.nl/

.. _Sundown: https://github.com/tanoku/sundown


Installation
------------

Cython is needed to compile Misaka.

With pip::

    pip install misaka

Or manually::

    python setup.py install


Example
-------

Very simple example::

    from misaka import Markdown, HtmlRenderer

    rndr = HtmlRenderer()
    md = Markdown(rndr)

    print md.render('some text')
