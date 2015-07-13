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

Or the lastest development version from Github::

    git clone https://github.com/FSX/misaka.git
    cd misaka
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


Renderers
^^^^^^^^^

A custom renderer cna be written by subclassing :class:`misaka.BaseRenderer` or
:class:`misaka.HtmlRenderer`. Here's a simple example that uses Pygments_ to
highlight code (houdini_ is used to escape the HTML)::

    import houdini as h
    import misaka as m
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name

    class HighlighterRenderer(m.HtmlRenderer):
        def blockcode(self, text, lang):
            if not lang:
                return '\n<pre>{}</code></pre>\n'.format(
                    h.escape_html(text.strip()))

            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter()

            return highlight(text, lexer, formatter)

    renderer = HighlighterRenderer()
    md = m.Markdown(renderer, extensions=m.EXT_FENCED_CODE)

    print(md.render("""
    Here is some code:

    ```python
    print(123)
    ```

    More code:

        print(123)
    """))


See ``tests/test_renderer.py`` for a complete renderer.

.. _Pygments: http://pygments.org
.. _houdini: https://github.com/FSX/houdini.py


Testing
-------

Assuming you've downloaded the source files. Run one of the following commands::

    python setup.py test  # or...
    python tests/runner.py


Writing tests
^^^^^^^^^^^^^

TODO


API
---

.. py:currentmodule:: misaka

.. autoclass:: BaseRenderer

    .. py:method:: blockcode(text, lang=None)

    .. py:method:: blockquote(content)

    .. py:method:: header(content, level)

    .. py:method:: hrule()

    .. py:method:: list(content, flags=0)

        Possible flags: LIST_ORDERED, LI_BLOCK

    .. py:method:: listitem(content, flags=0)

        Possible flags: LIST_ORDERED, LI_BLOCK

    .. py:method:: paragraph(content)

    .. py:method:: table(content)

    .. py:method:: table_header(content)

    .. py:method:: table_body(content)

    .. py:method:: table_row(content)

    .. py:method:: table_cell(content, flags=0)

        Possible flags: TABLE_ALIGNMASK, TABLE_ALIGN_LEFT, TABLE_ALIGN_RIGHT,
        TABLE_ALIGN_CENTER, TABLE_HEADER

    .. py:method:: footnotes(content)

    .. py:method:: footnote_def(content, num)

    .. py:method:: blockhtml(text)

    .. py:method:: autolink(link, type)

        TODO: type

    .. py:method:: codespan(text)

    .. py:method:: double_emphasis(content)

    .. py:method:: emphasis(content)

        NOTE: emphasis doesn't work with single underscores when underline
        is enabled.

    .. py:method:: underline(content)

    .. py:method:: highlight(content)

    .. py:method:: quote(content)

    .. py:method:: image(link, title=None, alt=None)

    .. py:method:: linebreak()

    .. py:method:: link(content, link, title=None)

    .. py:method:: triple_emphasis(content)

    .. py:method:: strikethrough(content)

    .. py:method:: superscript(content)

    .. py:method:: footnote_ref(num)

    .. py:method:: math(text, displaymode)

        TODO: displaymode

    .. py:method:: raw_html(text)

    .. py:method:: entity(text)

    .. py:method:: normal_text(text)

    .. py:method:: doc_header(inline_render)

    .. py:method:: doc_footer(inline_render)


.. autoclass:: HtmlRenderer
    :members:


.. autoclass:: Markdown
    :members:


.. autofunction:: html


.. autofunction:: smartypants


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
