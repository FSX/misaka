from inspect import getmembers, ismethod

from ._hoedown import lib, ffi


__all__ = [
    'html',
    'Markdown',
    'BaseRenderer',
    'HtmlRenderer'
]


def html(text, extensions=0, render_flags=0):
    ib = lib.hoedown_buffer_new(1024)
    ob = lib.hoedown_buffer_new(64)
    renderer = lib.hoedown_html_renderer_new(0, 0)
    document = lib.hoedown_document_new(renderer, 0, 16);

    lib.hoedown_buffer_puts(ib, text.encode('utf-8'))
    lib.hoedown_document_render(document, ob, ib.data, ib.size);
    lib.hoedown_buffer_free(ib);
    lib.hoedown_document_free(document);
    lib.hoedown_html_renderer_free(renderer);

    try:
        return ffi.string(ob.data, ob.size).decode('utf-8')
    finally:
        lib.hoedown_buffer_free(ob);


class Markdown:
    def __init__(self, renderer):
        # NOTE: Prevent the renderer from being garbage collected
        self.renderer = renderer

    def render(self, text):
        ib = lib.hoedown_buffer_new(1024)
        lib.hoedown_buffer_puts(ib, text.encode('utf-8'))

        ob = lib.hoedown_buffer_new(64)
        document = lib.hoedown_document_new(self.renderer.renderer, 0, 16);
        lib.hoedown_document_render(document, ob, ib.data, ib.size);

        lib.hoedown_buffer_free(ib);
        lib.hoedown_document_free(document);

        try:
            return ffi.string(ob.data, ob.size).decode('utf-8')
        finally:
            lib.hoedown_buffer_free(ob);


callback_signatures = {
    # block level callbacks - NULL skips the block
    'blockcode':    'void (*blockcode)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_buffer *lang, const hoedown_renderer_data *data)',
    'blockquote':   'void (*blockquote)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'header':       'void (*header)(hoedown_buffer *ob, const hoedown_buffer *content, int level, const hoedown_renderer_data *data)',
    'hrule':        'void (*hrule)(hoedown_buffer *ob, const hoedown_renderer_data *data)',
    'list':         'void (*list)(hoedown_buffer *ob, const hoedown_buffer *content, hoedown_list_flags flags, const hoedown_renderer_data *data)',
    'listitem':     'void (*listitem)(hoedown_buffer *ob, const hoedown_buffer *content, hoedown_list_flags flags, const hoedown_renderer_data *data)',
    'paragraph':    'void (*paragraph)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table':        'void (*table)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table_header': 'void (*table_header)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table_body':   'void (*table_body)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table_row':    'void (*table_row)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'table_cell':   'void (*table_cell)(hoedown_buffer *ob, const hoedown_buffer *content, hoedown_table_flags flags, const hoedown_renderer_data *data)',
    'footnotes':    'void (*footnotes)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'footnote_def': 'void (*footnote_def)(hoedown_buffer *ob, const hoedown_buffer *content, unsigned int num, const hoedown_renderer_data *data)',
    'blockhtml':    'void (*blockhtml)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data)',

    # span level callbacks - NULL or return 0 prints the span verbatim
    'autolink':        'int (*autolink)(hoedown_buffer *ob, const hoedown_buffer *link, hoedown_autolink_type type, const hoedown_renderer_data *data)',
    'codespan':        'int (*codespan)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data)',
    'double_emphasis': 'int (*double_emphasis)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'emphasis':        'int (*emphasis)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'underline':       'int (*underline)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'highlight':       'int (*highlight)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'quote':           'int (*quote)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'image':           'int (*image)(hoedown_buffer *ob, const hoedown_buffer *link, const hoedown_buffer *title, const hoedown_buffer *alt, const hoedown_renderer_data *data)',
    'linebreak':       'int (*linebreak)(hoedown_buffer *ob, const hoedown_renderer_data *data)',
    'link':            'int (*link)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_buffer *link, const hoedown_buffer *title, const hoedown_renderer_data *data)',
    'triple_emphasis': 'int (*triple_emphasis)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'strikethrough':   'int (*strikethrough)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'superscript':     'int (*superscript)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data)',
    'footnote_ref':    'int (*footnote_ref)(hoedown_buffer *ob, unsigned int num, const hoedown_renderer_data *data)',
    'math':            'int (*math)(hoedown_buffer *ob, const hoedown_buffer *text, int displaymode, const hoedown_renderer_data *data)',
    'raw_html':        'int (*raw_html)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data)',

    # low level callbacks - NULL copies input directly into the output
    'entity':      'void (*entity)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data);',
    'normal_text': 'void (*normal_text)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data);',

    # miscellaneous callbacks
    'doc_header': 'void (*doc_header)(hoedown_buffer *ob, int inline_render, const hoedown_renderer_data *data);',
    'doc_footer': 'void (*doc_footer)(hoedown_buffer *ob, int inline_render, const hoedown_renderer_data *data);',
}


# TODO: Do this in Python:
# static hoedown_renderer *
# null_renderer_new()
# {
#     hoedown_renderer *renderer;
#     renderer = hoedown_malloc(sizeof(hoedown_renderer));
#     memset(renderer, 0x0, sizeof(hoedown_renderer));

#     return renderer;
# }

# static void
# null_renderer_free(hoedown_renderer *renderer)
# {
#     free(renderer);
# }
class BaseRenderer:
    def __init__(self):
        # TODO: Make a null renderer.
        self.renderer = None
        self.set_callbacks()

    def set_callbacks(self):
        callbacks = []

        for name, func in getmembers(self, predicate=ismethod):
            signature = callback_signatures.get(name)
            if signature is None:
                continue

            wrapper = getattr(self, '_w_' + name)
            callback = ffi.callback(signature, wrapper)
            callbacks.append(callback)
            setattr(self.renderer, name, callback)

        # Prevent callbacks from being garbage collected.
        self._callbacks = callbacks

    def _w_blockcode(self, ob, text, lang, data):
        text = ffi.string(text.data, text.size).decode('utf-8')
        lang = ffi.string(lang.data, lang.size).decode('utf-8')
        result = self.blockcode(text, lang)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_blockquote(self, ob, content, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        result = self.blockquote(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_header(self, ob, content, level, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
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
        content = ffi.string(content.data, content.size).decode('utf-8')
        flags = int(flags)
        result = self.list(content, flags)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    # flags: LIST_ORDERED, LI_BLOCK.
    def _w_listitem(self, ob, content, flags, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        flags = int(flags)
        result = self.listitem(content, flags)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_paragraph(self, ob, content, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        result = self.paragraph(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_table(self, ob, content, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        result = self.table(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_table_header(self, ob, content, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        result = self.table_header(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_table_body(self, ob, content, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        result = self.table_body(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_table_row(self, ob, content, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        result = self.table_row(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_table_cell(self, ob, content, flags, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        flags = int(flags)
        result = self.table_row(content, flags)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_footnotes(self, ob, content, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        result = self.footnotes(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_footnote_def(self, ob, content, num, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        num = int(num)
        result = self.footnote_def(content, num)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_blockhtml(self, ob, text, data):
        text = ffi.string(text.data, text.size).decode('utf-8')
        result = self.blockhtml(text)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))

    def _w_emphasis(self, ob, content, data):
        content = ffi.string(content.data, content.size).decode('utf-8')
        result = self.emphasis(content)
        if result:
            lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
            return 1
        return 0


class HtmlRenderer(BaseRenderer):
    def __init__(self):
        self.renderer = lib.hoedown_html_renderer_new(0, 0)
        self.set_callbacks()

    def __del__(self):
        lib.hoedown_html_renderer_free(self.renderer)
