.. py:currentmodule:: misaka

Misaka
======

Misaka is a CFFI-based binding for Hoedown_, a fast markdown processing library
written in C. It features a fast HTML renderer and functionality to make custom
renderers (e.g. man pages or LaTeX).

See the :doc:`/changelog` for all changes.

.. _Hoedown: https://github.com/hoedown/hoedown


Installation
------------

Misaka has been tested on CPython 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, 3.6 and PyPy 2.6+.
CFFI 1.0 or newer is required. This means Misaka will not work on PyPy 2.5
and older versions.

If you're installing from source and are using Debian or a Debian derivative
(e.g. Ubuntu) make sure ``build-essential``, ``python-dev`` and ``libffi-dev``
are installed.

Install with pip::

    pip install misaka

Or grab the source from Github::

    git clone https://github.com/FSX/misaka.git
    cd misaka
    python setup.py install

Consult the `CFFI documentation`_ if you experience problems installing CFFI.

Use the following commands to install Misaka in Termux_::

    apt update
    apt upgrade
    apt install clang python python-dev libffi libffi-dev
    pip install misaka

.. _Termux: https://termux.com/
.. _CFFI documentation: https://cffi.readthedocs.org/en/latest/installation.html


Usage
-----

Very simple example:

.. code:: python

    import misaka as m
    print m.html('some other text')

Or:

.. code:: python

    from misaka import Markdown, HtmlRenderer

    rndr = HtmlRenderer()
    md = Markdown(rndr)

    print md('some text')

Here's a simple example that uses Pygments_ to highlight code (houdini_ is
used to escape the HTML):

.. code:: python

    import houdini as h
    import misaka as m
    from pygments import highlight
    from pygments.formatters import HtmlFormatter, ClassNotFound
    from pygments.lexers import get_lexer_by_name

    class HighlighterRenderer(m.HtmlRenderer):
        def blockcode(self, text, lang):
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ClassNotFound:
                lexer = None

            if lexer:
                formatter = HtmlFormatter()
                return highlight(text, lexer, formatter)
            # default
            return '\n<pre><code>{}</code></pre>\n'.format(
                                h.escape_html(text.strip()))

    renderer = HighlighterRenderer()
    md = m.Markdown(renderer, extensions=('fenced-code',))

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


Tests
-----

tidy_ is needed to run the tests. tox_ can be used to run the tests on
all supported Python versions with one command.

Run one of the following commands to install tidy::

    apt-get install tidy  # Debian and derivatives
    pacman -S tidyhtml    # Arch Linux

And run the tests with::

    python setup.py test

It's also possible to include or exclude tests. ``-i`` and ``-e`` accept a
comma separated list of testcases::

    # Only run MarkdownConformanceTest_10
    python setup.py test -i MarkdownConformanceTest_10

    # Or everything except MarkdownConformanceTest_10
    python setup.py test -e MarkdownConformanceTest_10

    # Or everything except MarkdownConformanceTest_10 and MarkdownConformanceTest_103
    python setup.py test -e MarkdownConformanceTest_10,MarkdownConformanceTest_103

``-l`` prints a list of all testcases::

    $ python setup.py test -l
    [... build output ...]
    MarkdownConformanceTest_10
    MarkdownConformanceTest_103
    BenchmarkLibraries
    ArgsToIntTest
    CustomRendererTest
    SmartypantsTest

And ``-b`` runs benchmarks (``-i`` and ``-e`` can also be used in
combination with ``-b``)::

    $ python setup.py test -b
    [... build output ...]
    >> BenchmarkLibraries
    test_hoep                     3270         1.00 s/t     305.91 us/op
    test_markdown                   20         1.23 s/t      61.44 ms/op
    test_markdown2                  10         3.29 s/t     329.34 ms/op
    test_misaka                   3580         1.00 s/t     280.01 us/op
    test_misaka_classes           3190         1.00 s/t     314.00 us/op
    test_mistune                    70         1.04 s/t      14.91 ms/o

What you see in the above output are the name, repetitions, total amount of
time (in seconds) and the time taken for an operation (one repetition).
A benchmark tries to stay within one second and runs a test for a minimum
of ten repetitions and tries another ten if there's time left.

.. _tidy: http://tidy.sourceforge.net
.. _tox: https://testrun.org/tox/


API
---

Extensions
^^^^^^^^^^

======================  ==========================
Name                    Constant
======================  ==========================
tables                  EXT_TABLES
fenced-code             EXT_FENCED_CODE
footnotes               EXT_FOOTNOTES
autolink                EXT_AUTOLINK
strikethrough           EXT_STRIKETHROUGH
underline               EXT_UNDERLINE
highlight               EXT_HIGHLIGHT
quote                   EXT_QUOTE
superscript             EXT_SUPERSCRIPT
math                    EXT_MATH
no-intra-emphasis       EXT_NO_INTRA_EMPHASIS
space-headers           EXT_SPACE_HEADERS
math-explicit           EXT_MATH_EXPLICIT
disable-indented-code   EXT_DISABLE_INDENTED_CODE
======================  ==========================


HTML render flags
^^^^^^^^^^^^^^^^^

==========  ==============
Name        Constant
==========  ==============
skip-html   HTML_SKIP_HTML
escape      HTML_ESCAPE
hard-wrap   HTML_HARD_WRAP
use-xhtml   HTML_USE_XHTML
==========  ==============


Functions
^^^^^^^^^

.. autofunction:: html


.. autofunction:: smartypants


.. autofunction:: escape_html


Classes
^^^^^^^

.. autoclass:: Markdown
    :members:


.. autoclass:: HtmlRenderer
    :members:


.. autoclass:: SaferHtmlRenderer
    :members:


.. autoclass:: HtmlTocRenderer
    :members:


.. autoclass:: BaseRenderer

    .. py:method:: blockcode(text, lang='')

        ``lang`` contains the language when fenced code blocks
        are enabled and a language is defined in ther code block.

    .. py:method:: blockquote(content)

    .. py:method:: header(content, level)

        ``level`` can be a humber from 1 to 6.

    .. py:method:: hrule()

    .. py:method:: list(content, is_ordered, is_block)

    .. py:method:: listitem(content, is_ordered, is_block)

    .. py:method:: paragraph(content)

    .. py:method:: table(content)

        Depends on the tables extension.

    .. py:method:: table_header(content)

        Depends on the tables extension.

    .. py:method:: table_body(content)

        Depends on the tables extension.

    .. py:method:: table_row(content)

        Depends on the tables extension.

    .. py:method:: table_cell(content, align, is_header)

        Depends on the tables extension.

        ``align`` can be empty, ``center``, ``left`` or ``right``.

    .. py:method:: footnotes(content)

        Depends on the footnotes extension.

    .. py:method:: footnote_def(content, num)

        Depends on the footnotes extension.

    .. py:method:: footnote_ref(num)

        Depends on the footnotes extension.

    .. py:method:: blockhtml(text)

    .. py:method:: autolink(link, is_email)

        Depends on the autolink extension.

    .. py:method:: codespan(text)

    .. py:method:: double_emphasis(content)

    .. py:method:: emphasis(content)

    .. py:method:: underline(content)

        Depends on the underline extension.

    .. py:method:: highlight(content)

        Depends on the highlight extension.

    .. py:method:: quote(content)

        Depends on the quote extension.

    .. py:method:: image(link, title='', alt='')

    .. py:method:: linebreak()

    .. py:method:: link(content, link, title='')

    .. py:method:: triple_emphasis(content)

    .. py:method:: strikethrough(content)

        Depends on the strikethrough extension.

    .. py:method:: superscript(content)

        Depends on the superscript extension.

    .. py:method:: math(text, displaymode)

        Depends on the math extension.

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
