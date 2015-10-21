# -*- coding: utf-8 -*-

from ._hoedown import lib, ffi
from .callbacks import python_callbacks, to_string
from .constants import *
from .utils import extension_map, html_flag_map, args_to_int, \
    deprecation, to_string


__all__ = [
    'html',
    'smartypants',
    'Markdown',
    'BaseRenderer',
    'HtmlRenderer',
    'HtmlTocRenderer',

    'args_to_int',
    'extension_map',
    'html_flag_map',

    'EXT_TABLES',
    'EXT_FENCED_CODE',
    'EXT_FOOTNOTES',
    'EXT_AUTOLINK',
    'EXT_STRIKETHROUGH',
    'EXT_UNDERLINE',
    'EXT_HIGHLIGHT',
    'EXT_QUOTE',
    'EXT_SUPERSCRIPT',
    'EXT_MATH',
    'EXT_NO_INTRA_EMPHASIS',
    'EXT_SPACE_HEADERS',
    'EXT_MATH_EXPLICIT',
    'EXT_DISABLE_INDENTED_CODE',

    'HTML_SKIP_HTML',
    'HTML_ESCAPE',
    'HTML_HARD_WRAP',
    'HTML_USE_XHTML',

    'LIST_ORDERED',
    'LI_BLOCK',

    'TABLE_ALIGN_LEFT',
    'TABLE_ALIGN_RIGHT',
    'TABLE_ALIGN_CENTER',
    'TABLE_ALIGNMASK',
    'TABLE_HEADER',

    'AUTOLINK_NORMAL',
    'AUTOLINK_EMAIL',
]


IUNIT = 1024
OUNIT = 64
MAX_NESTING = 16


def html(text, extensions=0, render_flags=0):
    """
    Convert markdown text to HTML.

    ``extensions`` can be a list or tuple of extensions (e.g.
    ``('fenced-code', 'footnotes', 'strikethrough')``) or an integer
    (e.g. ``EXT_FENCED_CODE | EXT_FOOTNOTES | EXT_STRIKETHROUGH``).

    ``render_flags`` can be a list or tuple of flags (e.g.
    ``('skip-html', 'hard-wrap')``) or an integer
    (e.g. ``HTML_SKIP_HTML | HTML_HARD_WRAP``).
    """
    extensions = args_to_int(extension_map, extensions)
    render_flags = args_to_int(html_flag_map, render_flags)

    ib = lib.hoedown_buffer_new(IUNIT)
    ob = lib.hoedown_buffer_new(OUNIT)
    renderer = lib.hoedown_html_renderer_new(render_flags, 0)
    document = lib.hoedown_document_new(renderer, extensions, 16);

    lib.hoedown_buffer_puts(ib, text.encode('utf-8'))
    lib.hoedown_document_render(document, ob, ib.data, ib.size);
    lib.hoedown_buffer_free(ib);
    lib.hoedown_document_free(document);
    lib.hoedown_html_renderer_free(renderer);

    try:
        return to_string(ob)
    finally:
        lib.hoedown_buffer_free(ob);


def smartypants(text):
    """
    Transforms sequences of characters into HTML entities.

    ===================================  =====================  =========
    Markdown                             HTML                   Result
    ===================================  =====================  =========
    ``'s`` (s, t, m, d, re, ll, ve)      &rsquo;s               ’s
    ``"Quotes"``                         &ldquo;Quotes&rdquo;   “Quotes”
    ``---``                              &mdash;                —
    ``--``                               &ndash;                –
    ``...``                              &hellip;               …
    ``. . .``                            &hellip;               …
    ``(c)``                              &copy;                 ©
    ``(r)``                              &reg;                  ®
    ``(tm)``                             &trade;                ™
    ``3/4``                              &frac34;               ¾
    ``1/2``                              &frac12;               ½
    ``1/4``                              &frac14;               ¼
    ===================================  =====================  =========
    """
    byte_str = text.encode('utf-8')
    ob = lib.hoedown_buffer_new(OUNIT)
    lib.hoedown_html_smartypants(ob, byte_str, len(byte_str))

    try:
        return to_string(ob)
    finally:
        lib.hoedown_buffer_free(ob);


class Markdown(object):
    """
    Parses markdown text and renders it using the given renderer.

    ``extensions`` can be a list or tuple of extensions (e.g.
    ``('fenced-code', 'footnotes', 'strikethrough')``) or an integer
    (e.g. ``EXT_FENCED_CODE | EXT_FOOTNOTES | EXT_STRIKETHROUGH``).
    """
    def __init__(self, renderer, extensions=0):
        self.renderer = renderer
        self.extensions = args_to_int(extension_map, extensions)

    def __call__(self, text):
        """
        Parses and renders markdown text.
        """
        ib = lib.hoedown_buffer_new(IUNIT)
        lib.hoedown_buffer_puts(ib, text.encode('utf-8'))

        ob = lib.hoedown_buffer_new(OUNIT)
        document = lib.hoedown_document_new(
            self.renderer.renderer,
            self.extensions,
            MAX_NESTING);
        lib.hoedown_document_render(document, ob, ib.data, ib.size);

        lib.hoedown_buffer_free(ib)
        lib.hoedown_document_free(document)

        try:
            return to_string(ob)
        finally:
            lib.hoedown_buffer_free(ob);


class BaseRenderer(object):
    def __init__(self):
        self.renderer = ffi.new('hoedown_renderer *')
        self._renderer_handle = ffi.new_handle(self)

        for name in python_callbacks.keys():
            if hasattr(self, name):
                setattr(self.renderer, name, python_callbacks[name])
            else:
                setattr(self.renderer, name, ffi.NULL)

        # Store the render class' handle in the render data.
        self._data = ffi.new('hoedown_renderer_data *')
        self.renderer.opaque = self._data
        ffi.cast('hoedown_renderer_data *', self.renderer.opaque).opaque = \
            self._renderer_handle


class HtmlRenderer(BaseRenderer):
    """
    A wrapper for the HTML renderer that's included in Hoedown.

    ``render_flags`` can be a list or tuple of flags (e.g.
    ``('skip-html', 'hard-wrap')``) or an integer
    (e.g. ``HTML_SKIP_HTML | HTML_HARD_WRAP``).

    ``nesting_level`` limits what's included in the table of contents.
    The default value is 0, no headers.

    An instance of the ``HtmlRenderer`` can not be shared with multiple
    :py:class:`Markdown` instances, because it carries state that's changed
    by the ``Markdown`` instance.
    """
    def __init__(self, flags=0, nesting_level=0):
        flags = args_to_int(html_flag_map, flags)
        self.renderer = self._new_renderer(flags, nesting_level)
        self._renderer_handle = ffi.new_handle(self)

        # Store the render class' handle in the render state.
        state = ffi.cast('hoedown_renderer_data *', self.renderer.opaque)
        state.opaque = self._renderer_handle

        for name in python_callbacks.keys():
            if hasattr(self, name):
                setattr(self.renderer, name, python_callbacks[name])

    def _new_renderer(self, flags, nesting_level):
        return lib.hoedown_html_renderer_new(flags, nesting_level)

    def __del__(self):
        lib.hoedown_html_renderer_free(self.renderer)


class HtmlTocRenderer(HtmlRenderer):
    """
    A wrapper for the HTML table of contents renderer that's included in Hoedown.

    ``nesting_level`` limits what's included in the table of contents.
    The default value is 6, all headers.

    An instance of the ``HtmlTocRenderer`` can not be shared with multiple
    :py:class:`Markdown` instances, because it carries state that's changed
    by the ``Markdown`` instance.
    """
    def __init__(self, nesting_level=6):
        HtmlRenderer.__init__(self, 0, nesting_level)

    def _new_renderer(self, flags, nesting_level):
        return lib.hoedown_html_toc_renderer_new(nesting_level)
