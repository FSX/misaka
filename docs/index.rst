Misaka
======

Misaka is a CFFI-based binding for Hoedown_, a fast markdown processing library
written in C. It features a fast HTML renderer and functionality to make custom
renderers (e.g. man pages or LaTeX).


Changelog
---------

**2.0.0 (2015-07-??)**

- Rewrite. CFFI_ and Hoedown_ instead of Cython_ and Sundown_.
- Remove pre- and postprocessor support.
- Smartypants is a normal function instead of a postprocessor.

See the full changelog at :doc:`/changelog`.

.. _Hoedown: https://github.com/hoedown/hoedown
.. _Sundown: https://github.com/vmg/sundown
.. _CFFI: https://cffi.readthedocs.org
.. _Cython: http://cython.org/


Installation
------------

Misaka has been tested on CPython 2.7, 3.2, 3.3, 3.4 and PyPy 2.6. It needs
CFFI 1.0 or newer, because of this it will not work on PyPy 2.5 and older.

With pip::

    pip install misaka

Or manually::

    python setup.py install


Usage
-----

Very simple example::

    from misaka import Markdown, HtmlRenderer

    rndr = HtmlRenderer()
    md = Markdown(rndr)

    print md.render('some text')

Or::

    import misaka as m
    print m.html('some other text')


Testing
-------

Run one of the following commands::

	python setup.py test  # or...
	python tests/runner.py


API
---

TODO



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
