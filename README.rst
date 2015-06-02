Misaka
======

.. image:: https://secure.travis-ci.org/FSX/misaka.png?branch=master

A CFFI binding for Hoedown_, a markdown parsing library.

Documentation can be found at: http://misaka.61924.nl/

.. _Hoedown: https://github.com/hoedown/hoedown


Installation
------------

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

Or::

    import misaka as m
    print m.html('some other text')
