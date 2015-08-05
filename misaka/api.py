# -*- coding: utf-8 -*-

import sys
import operator as op
from inspect import getmembers, ismethod

from ._hoedown import lib, ffi

try:
    reduce
except NameError:
    from functools import reduce


__all__ = [
    'html',
    'smartypants',
    'Markdown',
    'BaseRenderer',
    'HtmlRenderer',
    'HtmlTocRenderer',

    'dict_to_int',
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


def _set_constants():
    is_int = lambda n: isinstance(n, int)

    for name, value in getmembers(lib, is_int):
        if not name.startswith('HOEDOWN_'):
            continue
        setattr(sys.modules[__name__], name[8:], value)


if not hasattr(sys.modules[__name__], 'EXT_TABLES'):
    _set_constants()


extension_map = {
    'tables': EXT_TABLES,
    'fenced-code': EXT_FENCED_CODE,
    'footnotes': EXT_FOOTNOTES,
    'autolink': EXT_AUTOLINK,
    'strikethrough': EXT_STRIKETHROUGH,
    'underline': EXT_UNDERLINE,
    'highlight': EXT_HIGHLIGHT,
    'quote': EXT_QUOTE,
    'superscript': EXT_SUPERSCRIPT,
    'math': EXT_MATH,
    'no-intra-emphasis': EXT_NO_INTRA_EMPHASIS,
    'space-headers': EXT_SPACE_HEADERS,
    'math-explicit': EXT_MATH_EXPLICIT,
    'disable-indented-code': EXT_DISABLE_INDENTED_CODE,
}

html_flag_map = {
    'skip-html': HTML_SKIP_HTML,
    'escape': HTML_ESCAPE,
    'hard-wrap': HTML_HARD_WRAP,
    'use-xhtml': HTML_USE_XHTML,
}


IUNIT = 1024
OUNIT = 64
MAX_NESTING = 16


def to_string(buffer):
    if buffer == ffi.NULL or buffer.size == 0:
        return ''
    return ffi.string(buffer.data, buffer.size).decode('utf-8')


def dict_to_int(mapping, argument):
    """
    Reduce a dictionary to an integer.

    This function is used to reduce a dictionary (e.g. Markdown extensions,
    HTML render flags.) to an integer by OR'ing the values with eachother.
    """
    if isinstance(argument, int):
        return argument
    elif isinstance(argument, (tuple, list)):
        return reduce(op.or_, [mapping[n] for n in argument if n in mapping])

    raise TypeError('argument must be a list of strings or an int')


def html(text, extensions=0, render_flags=0):
    """
    Convert markdown text to HTML.
    """
    render_flags = dict_to_int(html_flag_map, render_flags)

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


class Markdown:
    """
    Parses markdown text and renders it using the given renderer.
    """
    def __init__(self, renderer, extensions=0):
        self.renderer = renderer
        self.extensions = dict_to_int(extension_map, extensions)

    def __call__(self, text):
        """
        Parses and renders markdown text.
        """
        ib = lib.hoedown_buffer_new(IUNIT)
        lib.hoedown_buffer_puts(ib, text.encode('utf-8'))

        ob = lib.hoedown_buffer_new(OUNIT)
        document = lib.hoedown_document_new(self.renderer.renderer, self.extensions, MAX_NESTING);
        lib.hoedown_document_render(document, ob, ib.data, ib.size);

        lib.hoedown_buffer_free(ib)
        lib.hoedown_document_free(document)

        try:
            return to_string(ob)
        finally:
            lib.hoedown_buffer_free(ob);


_callback_signatures = {
    # block level callbacks - NULL skips the block
    'blockcode':    'void(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_buffer *lang, const hoedown_renderer_data *data)',
    'blockquote':   'void(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'header':       'void(hoedown_buffer *ob, const hoedown_buffer *content, int level, const hoedown_renderer_data *data)',
    'hrule':        'void(hoedown_buffer *ob, const hoedown_renderer_data *data)',
    'list':         'void(hoedown_buffer *ob, const hoedown_buffer *content, hoedown_list_flags flags, const hoedown_renderer_data *data)',
    'listitem':     'void(hoedown_buffer *ob, const hoedown_buffer *content, hoedown_list_flags flags, const hoedown_renderer_data *data)',
    'paragraph':    'void(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table':        'void(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table_header': 'void(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table_body':   'void(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table_row':    'void(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table_cell':   'void(hoedown_buffer *ob, const hoedown_buffer *content, hoedown_table_flags flags, const hoedown_renderer_data *data)',
    'footnotes':    'void(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'footnote_def': 'void(hoedown_buffer *ob, const hoedown_buffer *content, unsigned int num, const hoedown_renderer_data *data)',
    'blockhtml':    'void(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data)',

    # span level callbacks - NULL or return 0 prints the span verbatim
    'autolink':        'int(hoedown_buffer *ob, const hoedown_buffer *link, hoedown_autolink_type type, const hoedown_renderer_data *data)',
    'codespan':        'int(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data)',
    'double_emphasis': 'int(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'emphasis':        'int(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'underline':       'int(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'highlight':       'int(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'quote':           'int(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'image':           'int(hoedown_buffer *ob, const hoedown_buffer *link, const hoedown_buffer *title, const hoedown_buffer *alt, const hoedown_renderer_data *data)',
    'linebreak':       'int(hoedown_buffer *ob, const hoedown_renderer_data *data)',
    'link':            'int(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_buffer *link, const hoedown_buffer *title, const hoedown_renderer_data *data)',
    'triple_emphasis': 'int(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'strikethrough':   'int(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'superscript':     'int(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'footnote_ref':    'int(hoedown_buffer *ob, unsigned int num, const hoedown_renderer_data *data)',
    'math':            'int(hoedown_buffer *ob, const hoedown_buffer *text, int displaymode, const hoedown_renderer_data *data)',
    'raw_html':        'int(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data)',

    # low level callbacks - NULL copies input directly into the output
    'entity':      'void(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data)',
    'normal_text': 'void(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data)',

    # miscellaneous callbacks
    'doc_header': 'void(hoedown_buffer *ob, int inline_render, const hoedown_renderer_data *data)',
    'doc_footer': 'void(hoedown_buffer *ob, int inline_render, const hoedown_renderer_data *data)',
}


class BaseRenderer:
    def __init__(self):
        # Use a noop method as a placeholder for render methods that are
        # implemented so there's no need to check if a render method exists
        # in a callback.
        for attr in _callback_signatures.keys():
            if not hasattr(self, attr):
                setattr(self, attr, self.noop)

        self._callbacks = {k: ffi.callback(v, getattr(self, '_w_' + k))
            for k, v in _callback_signatures.items()}
        self.renderer = ffi.new('hoedown_renderer *', self._callbacks)

    def noop(self, *args, **kwargs):
        return None

    def _w_blockcode(self, ob, text, lang, data):
        text = to_string(text)
        lang = to_string(lang)

        result = self.blockcode(text, lang)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_blockquote(self, ob, content, data):
        content = to_string(content)
        result = self.blockquote(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_header(self, ob, content, level, data):
        content = to_string(content)
        level = int(level)
        result = self.header(content, level)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_hrule(self, ob, data):
        result = self.hrule()
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    # flags: LIST_ORDERED, LI_BLOCK.
    def _w_list(self, ob, content, flags, data):
        content = to_string(content)
        flags = int(flags)
        result = self.list(content, flags)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    # flags: LIST_ORDERED, LI_BLOCK.
    def _w_listitem(self, ob, content, flags, data):
        content = to_string(content)
        flags = int(flags)
        result = self.listitem(content, flags)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_paragraph(self, ob, content, data):
        content = to_string(content)
        result = self.paragraph(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_table(self, ob, content, data):
        content = to_string(content)
        result = self.table(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_table_header(self, ob, content, data):
        content = to_string(content)
        result = self.table_header(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_table_body(self, ob, content, data):
        content = to_string(content)
        result = self.table_body(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_table_row(self, ob, content, data):
        content = to_string(content)
        result = self.table_row(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    # flags: TABLE_ALIGNMASK, TABLE_ALIGN_LEFT, TABLE_ALIGN_RIGHT,
    #        TABLE_ALIGN_CENTER, TABLE_HEADER
    def _w_table_cell(self, ob, content, flags, data):
        content = to_string(content)
        flags = int(flags)
        result = self.table_cell(content, flags)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_footnotes(self, ob, content, data):
        content = to_string(content)
        result = self.footnotes(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_footnote_def(self, ob, content, num, data):
        content = to_string(content)
        num = int(num)
        result = self.footnote_def(content, num)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_blockhtml(self, ob, text, data):
        text = ffi.string(text.data, text.size).decode('utf-8')
        result = self.blockhtml(text)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_autolink(self, ob, link, type, data):
        link = ffi.string(link.data, link.size).decode('utf-8')
        type = int(type)
        result = self.autolink(link, type)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_codespan(self, ob, text, data):
        text = ffi.string(text.data, text.size).decode('utf-8')
        result = self.codespan(text)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_double_emphasis(self, ob, content, data):
        content = to_string(content)
        result = self.double_emphasis(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_emphasis(self, ob, content, data):
        content = to_string(content)
        result = self.emphasis(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_underline(self, ob, content, data):
        content = to_string(content)
        result = self.underline(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_highlight(self, ob, content, data):
        content = to_string(content)
        result = self.highlight(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_quote(self, ob, content, data):
        content = to_string(content)
        result = self.quote(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_image(self, ob, link, title, alt, data):
        link = to_string(link)
        title = to_string(title)
        alt = to_string(alt)
        result = self.image(link, title, alt)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_linebreak(self, ob, data):
        result = self.linebreak()
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_link(self, ob, content, link, title, data):
        content = to_string(content)
        link = to_string(link)
        title = to_string(title)
        result = self.link(content, link, title)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_triple_emphasis(self, ob, content, data):
        content = to_string(content)
        result = self.triple_emphasis(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_strikethrough(self, ob, content, data):
        content = to_string(content)
        result = self.strikethrough(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_superscript(self, ob, content, data):
        content = to_string(content)
        result = self.superscript(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_footnote_ref(self, ob, num, data):
        num = int(num)
        result = self.footnote_ref(num)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_math(self, ob, text, displaymode, data):
        text = to_string(text)
        displaymode = int(displaymode)
        result = self.math(text, displaymode)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_raw_html(self, ob, text, data):
        text = to_string(text)
        result = self.raw_html(text)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0

    def _w_entity(self, ob, text, data):
        text = to_string(text)
        result = self.entity(text)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_normal_text(self, ob, text, data):
        text = to_string(text)
        result = self.normal_text(text)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_doc_header(self, ob, inline_render, data):
        inline_render = int(inline_render)
        result = self.doc_header(inline_render)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_doc_footer(self, ob, inline_render, data):
        inline_render = int(inline_render)
        result = self.doc_footer(inline_render)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


class HtmlRenderer(BaseRenderer):
    """
    A wrapper for the HTML renderer that's included in Hoedown.

    ``nesting_level`` limits what's included in the table of contents.
    The default value is 0, no headers.

    An instance of the ``HtmlRenderer`` can not be shared with multiple
    :py:class:`Markdown` instances, because it carries state that's changed
    by the ``Markdown`` instance.
    """
    def __init__(self, flags=0, nesting_level=0):
        flags = dict_to_int(html_flag_map, flags)
        self.renderer = self._new_renderer(flags, nesting_level)
        callbacks = []

        for name, signature in _callback_signatures.items():
            if not hasattr(self, name):
                continue

            wrapper = getattr(self, '_w_' + name)
            callback = ffi.callback(signature, wrapper)
            callbacks.append(callback)
            setattr(self.renderer, name, callback)

        # Prevent garbage collection of callbacks.
        self._callbacks = callbacks

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
