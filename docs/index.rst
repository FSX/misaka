.. py:currentmodule:: misaka

Documentation
=============

Misaka is a CFFI-based binding for Hoedown_, a fast markdown processing library
written in C. It features a fast HTML renderer and functionality to make custom
renderers (e.g. man pages or LaTeX).


Changelog
---------

**2.0.0b2 (2015-08-??)**

- Rename ``Markdown.render`` to ``Markdown.__call__``.

**2.0.0b1 (2015-07-18)**

- Rewrite. CFFI_ and Hoedown_ instead of Cython_ and Sundown_.
- Remove pre- and postprocessor support.
- Smartypants is a normal function instead of a postprocessor.
- Documentation now uses Sphinx_.

See the full changelog at :doc:`/changelog`.

.. _Hoedown: https://github.com/hoedown/hoedown
.. _Sundown: https://github.com/vmg/sundown
.. _CFFI: https://cffi.readthedocs.org
.. _Cython: http://cython.org/
.. _Sphinx: http://sphinx-doc.org


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

And run the tests::

    python setup.py test  # or...
    python tests/run_tests.py


Usage
-----

Very simple example:

.. code:: python

    from misaka import Markdown, HtmlRenderer

    rndr = HtmlRenderer()
    md = Markdown(rndr)

    print md('some text')

Or:

.. code:: python

    import misaka as m
    print m.html('some other text')

Here's a simple example that uses Pygments_ to highlight code (houdini_ is
used to escape the HTML):

.. code:: python

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

    print(md("""
    Here is some code:

    ```python
    print(123)
    ```

    More code:

        print(123)
    """))

The above code listing subclasses :py:class:`HtmlRenderer` and implements
a :py:meth:`BaseRenderer.blockcode` method. See ``tests/test_renderer.py``
for a renderer with all its methods implemented.

.. _Pygments: http://pygments.org
.. _houdini: https://github.com/FSX/houdini.py


API
---

Extensions
^^^^^^^^^^

.. py:data:: EXT_TABLES
.. py:data:: EXT_FENCED_CODE
.. py:data:: EXT_FOOTNOTES
.. py:data:: EXT_AUTOLINK
.. py:data:: EXT_STRIKETHROUGH
.. py:data:: EXT_UNDERLINE
.. py:data:: EXT_HIGHLIGHT
.. py:data:: EXT_QUOTE
.. py:data:: EXT_SUPERSCRIPT
.. py:data:: EXT_MATH
.. py:data:: EXT_NO_INTRA_EMPHASIS
.. py:data:: EXT_SPACE_HEADERS
.. py:data:: EXT_MATH_EXPLICIT
.. py:data:: EXT_DISABLE_INDENTED_CODE


HTML render flags
^^^^^^^^^^^^^^^^^

.. py:data:: HTML_SKIP_HTML
.. py:data:: HTML_ESCAPE
.. py:data:: HTML_HARD_WRAP
.. py:data:: HTML_USE_XHTML


Render method flags
^^^^^^^^^^^^^^^^^^^

These constants are passed to individual render methods as flags.

.. py:data:: LIST_ORDERED
.. py:data:: LI_BLOCK

.. py:data:: TABLE_ALIGN_LEFT
.. py:data:: TABLE_ALIGN_RIGHT
.. py:data:: TABLE_ALIGN_CENTER
.. py:data:: TABLE_ALIGNMASK
.. py:data:: TABLE_HEADER

.. py:data:: AUTOLINK_NORMAL
.. py:data:: AUTOLINK_EMAIL


Classes
^^^^^^^

.. autoclass:: BaseRenderer

    .. py:method:: blockcode(text, lang='')

        ``lang`` contains the language when fenced code blocks
        (:py:const:`EXT_FENCED_CODE`) are enabled and a language is
        defined in ther code block.

    .. py:method:: blockquote(content)

    .. py:method:: header(content, level)

        ``level`` can be a humber from 1 to 6.

    .. py:method:: hrule()

    .. py:method:: list(content, flags=0)

        ``flags`` can contain the following flags:

        - :py:const:`LIST_ORDERED`: An ordered list.
        - :py:const:`LI_BLOCK`: The contents of list items contain block
          elements (e.g. paragraphs).

    .. py:method:: listitem(content, flags=0)

        ``flags`` can contain the following flags:

        - :py:const:`LIST_ORDERED`: An ordered list.
        - :py:const:`LI_BLOCK`: The contents of list items contain block
          elements (e.g. paragraphs).

    .. py:method:: paragraph(content)

    .. py:method:: table(content)

        Depends on :py:const:`EXT_TABLES`.

    .. py:method:: table_header(content)

        Depends on :py:const:`EXT_TABLES`.

    .. py:method:: table_body(content)

        Depends on :py:const:`EXT_TABLES`.

    .. py:method:: table_row(content)

        Depends on :py:const:`EXT_TABLES`.

    .. py:method:: table_cell(content, flags=0)

        Depends on :py:const:`EXT_TABLES`.

        ``flags`` can contain the following flags:

        - :py:const:`TABLE_ALIGNMASK`: Alignment of the table cell.
        - :py:const:`TABLE_HEADER`: Table cell is located in the table header.

        ``TABLE_ALIGNMASK`` can be used to check what the alignment of the
        cell is. Here's an example:

        .. code:: python

            align_bit = flags & misaka.TABLE_ALIGNMASK

            if align_bit == misaka.TABLE_ALIGN_CENTER:
                align = 'center'
            elif align_bit == misaka.TABLE_ALIGN_LEFT:
                align = 'left'
            elif align_bit == misaka.TABLE_ALIGN_RIGHT:
                align = 'right'
            else:
                align = ''

    .. py:method:: footnotes(content)

        Depends on :py:const:`EXT_FOOTNOTES`.

    .. py:method:: footnote_def(content, num)

        Depends on :py:const:`EXT_FOOTNOTES`.

    .. py:method:: footnote_ref(num)

        Depends on :py:const:`EXT_FOOTNOTES`.

    .. py:method:: blockhtml(text)

    .. py:method:: autolink(link, type)

        Depends on :py:const:`EXT_AUTOLINK`.

        ``type`` can be :py:const:`AUTOLINK_NORMAL` or
        :py:const:`AUTOLINK_EMAIL`.

    .. py:method:: codespan(text)

    .. py:method:: double_emphasis(content)

    .. py:method:: emphasis(content)

    .. py:method:: underline(content)

        Depends on :py:const:`EXT_UNDERLINE`.

    .. py:method:: highlight(content)

        Depends on :py:const:`EXT_HIGHLIGHT`.

    .. py:method:: quote(content)

        Depends on :py:const:`EXT_QUOTE`.

    .. py:method:: image(link, title='', alt='')

    .. py:method:: linebreak()

    .. py:method:: link(content, link, title='')

    .. py:method:: triple_emphasis(content)

    .. py:method:: strikethrough(content)

        Depends on :py:const:`EXT_STRIKETHROUGH`.

    .. py:method:: superscript(content)

        Depends on :py:const:`EXT_SUPERSCRIPT`.

    .. py:method:: math(text, displaymode)

        Depends on :py:const:`EXT_MATH`.

        ``displaymode`` can be ``0`` or ``1``. This is how
        :py:class:`HtmlRenderer` handles it:

        .. code:: python

            if displaymode == 1:
                return '\\[{}\\]'.format(text)
            else:  # displaymode == 0
                return '\\({}\\)'.format(text)

    .. py:method:: raw_html(text)

    .. py:method:: entity(text)

    .. py:method:: normal_text(text)

    .. py:method:: doc_header(inline_render)

    .. py:method:: doc_footer(inline_render)


.. autoclass:: HtmlRenderer
    :members:


.. autoclass:: HtmlTocRenderer
    :members:


.. autoclass:: Markdown
    :members:


Functions
^^^^^^^^^

.. autofunction:: html

.. autofunction:: smartypants
