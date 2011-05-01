Pantyshot
=========

A Python extension for [Upskirt][1].

 [1]: https://github.com/FSX/pantyshot


Installation
------------

    python setup.py install


Usage
-----

    import pantyshot

    pantyshot.markdown('Hello, world!')

With extensions and render flags.

    import pantyshot as p

    pantyshot.markdown(
        'Hello, world!',
        p.EXT_AUTOLINK | p.EXT_TABLES,
        p.XHTML_EXPAND_TABS | p.XHTML_SMARTYPANTS
    )

In combination with `functools.partial`.

    import functools
    import pantyshot as p

    markdown = functools.partial(
        p.markdown,
        extensions=p.EXT_AUTOLINK | p.EXT_TABLES,
        render_flags=p.XHTML_EXPAND_TABS | p.XHTML_SMARTYPANTS
    )
    markdown('Awesome!')


Extensions & render flags
-------------------------

Extensions:

    EXT_AUTOLINK
    EXT_LAX_HTML_BLOCKS
    EXT_TABLES
    EXT_NO_INTRA_EMPHASIS
    EXT_STRIKETHROUGH
    EXT_FENCED_CODE

Render flags:

    XHTML_GITHUB_BLOCKCODE
    XHTML_SMARTYPANTS
    XHTML_SKIP_HTML
    XHTML_SKIP_STYLE
    XHTML_HARD_WRAP
    XHTML_TOC
    XHTML_SKIP_LINKS
    XHTML_SAFELINK
    XHTML_SKIP_IMAGES
    XHTML_EXPAND_TABS

