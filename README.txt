Misaka
======

A Python binding for Upskirt_.

.. _Upskirt: https://github.com/tanoku/upskirt


Documentation can be found at: http://misaka.61924.nl/


Installation
------------

With pip::

    pip install misaka

Or manually::

    python setup.py install


Usage
-----

Without any extensions or flags enabled::

    import misaka

    misaka.html('Hello, world!')

With extensions and render flags::

    import misaka as m

    m.html(
        'Hello, world!',
        m.EXT_AUTOLINK | m.EXT_TABLES,
        m.HTML_EXPAND_TABS
    )

In combination with ``functools.partial``::

    import functools
    import misaka as m

    markdown = functools.partial(
        m.html,
        extensions=m.EXT_AUTOLINK | m.EXT_TABLES,
        render_flags=p.HTML_EXPAND_TABS
    )
    markdown('Awesome!')

Or generate a table of contents::

    misaka.toc('''
    # Header one

    Some text here.

    ## Header two

    Some more text
    ''')


Extensions & render flags
-------------------------

Extensions::

    EXT_AUTOLINK
    EXT_LAX_HTML_BLOCKS
    EXT_TABLES
    EXT_NO_INTRA_EMPHASIS
    EXT_STRIKETHROUGH
    EXT_FENCED_CODE
    EXT_SPACE_HEADERS

Render flags::

    HTML_GITHUB_BLOCKCODE
    HTML_SKIP_HTML
    HTML_SKIP_STYLE
    HTML_HARD_WRAP
    HTML_TOC
    HTML_SKIP_LINKS
    HTML_SAFELINK
    HTML_SKIP_IMAGES
    HTML_EXPAND_TABS
    HTML_USE_XHTML
    HTML_SMARTYPANTS
