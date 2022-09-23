**WARNING**: Misaka is not being maintained anymore. I've not been able to find time to to properly maintain this project. Consider using `mistletoe`_ or `Mistune`_.

.. _mistletoe: https://github.com/miyuchina/mistletoe
.. _Mistune: https://github.com/lepture/mistune

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


Professional support
====================

Professional support for Misaka is available as part of the `Tidelift
Subscription`_. Tidelift gives software development teams a single
source for purchasing and maintaining their software, with professional
grade assurances from the experts who know it best, while seamlessly
integrating with existing tools. By subscribing you will help support
Misaka future development. Alternatively consider making a small
`donation`_.

.. _Tidelift Subscription: https://tidelift.com/subscription/pkg/pypi-misaka?utm_source=pypi-misaka&utm_medium=referral&utm_campaign=readme
.. _`donation`: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FB6NWEJC87BJY&currency_code=EUR&source=url


Installation
------------

Misaka has been tested on CPython 2.7, 3.5, 3.6, 3.7, 3.8 and PyPy 2.7
and 3.5. It needs CFFI 1.12.0 or newer, because of this it will not work
on PyPy 2.5 and older.

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


Security contact information
----------------------------

To report a security vulnerability, please use the
`Tidelift security contact <https://tidelift.com/security>`_.
Tidelift will coordinate the fix and disclosure.
