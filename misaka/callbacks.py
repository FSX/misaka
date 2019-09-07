# -*- coding: utf-8 -*-

from ._hoedown import lib, ffi
from .constants import *
from .utils import to_string


@ffi.def_extern()
def _misaka_blockcode(ob, text, lang, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    text = to_string(text)
    lang = to_string(lang)

    result = renderer.blockcode(text, lang)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_blockquote(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.blockquote(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_header(ob, content, level, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    level = int(level)
    result = renderer.header(content, level)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_hrule(ob, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    result = renderer.hrule()
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


# flags: LIST_ORDERED, LI_BLOCK.
@ffi.def_extern()
def _misaka_list(ob, content, flags, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    flags = int(flags)
    is_ordered = flags & LIST_ORDERED != 0
    is_block = flags & LI_BLOCK != 0
    result = renderer.list(content, is_ordered, is_block)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


# flags: LIST_ORDERED, LI_BLOCK.
@ffi.def_extern()
def _misaka_listitem(ob, content, flags, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    flags = int(flags)
    is_ordered = flags & LIST_ORDERED != 0
    is_block = flags & LI_BLOCK != 0
    result = renderer.listitem(content, is_ordered, is_block)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_paragraph(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.paragraph(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_table(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.table(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_table_header(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.table_header(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_table_body(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.table_body(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_table_row(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.table_row(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


# flags: TABLE_ALIGNMASK, TABLE_ALIGN_LEFT, TABLE_ALIGN_RIGHT,
#        TABLE_ALIGN_CENTER, TABLE_HEADER
@ffi.def_extern()
def _misaka_table_cell(ob, content, flags, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    flags = int(flags)
    is_header = flags & TABLE_HEADER != 0
    align_bit = flags & TABLE_ALIGNMASK

    if align_bit == TABLE_ALIGN_CENTER:
        align = 'center'
    elif align_bit == TABLE_ALIGN_LEFT:
        align = 'left'
    elif align_bit == TABLE_ALIGN_RIGHT:
        align = 'right'
    else:
        align = ''

    result = renderer.table_cell(content, align, is_header)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_footnotes(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.footnotes(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_footnote_def(ob, content, num, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    num = int(num)
    result = renderer.footnote_def(content, num)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_blockhtml(ob, text, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    text = to_string(text)
    result = renderer.blockhtml(text)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_autolink(ob, link, type, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    link = to_string(link)
    is_email = int(type) & AUTOLINK_EMAIL != 0
    result = renderer.autolink(link, is_email)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_codespan(ob, text, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    text = to_string(text)
    result = renderer.codespan(text)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_double_emphasis(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.double_emphasis(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_emphasis(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.emphasis(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_underline(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.underline(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_highlight(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.highlight(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_quote(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.quote(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_image(ob, link, title, alt, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    link = to_string(link)
    title = to_string(title)
    alt = to_string(alt)
    result = renderer.image(link, title, alt)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_linebreak(ob, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    result = renderer.linebreak()
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_link(ob, content, link, title, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    link = to_string(link)
    title = to_string(title)
    result = renderer.link(content, link, title)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_triple_emphasis(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.triple_emphasis(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_strikethrough(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.strikethrough(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_superscript(ob, content, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    content = to_string(content)
    result = renderer.superscript(content)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_footnote_ref(ob, num, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    num = int(num)
    result = renderer.footnote_ref(num)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_math(ob, text, displaymode, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    text = to_string(text)
    displaymode = int(displaymode)
    result = renderer.math(text, displaymode)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_raw_html(ob, text, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    text = to_string(text)
    result = renderer.raw_html(text)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))
        return 1
    return 0


@ffi.def_extern()
def _misaka_entity(ob, text, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    text = to_string(text)
    result = renderer.entity(text)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_normal_text(ob, text, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    text = to_string(text)
    result = renderer.normal_text(text)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_doc_header(ob, inline_render, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    inline_render = int(inline_render)
    result = renderer.doc_header(inline_render)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


@ffi.def_extern()
def _misaka_doc_footer(ob, inline_render, data):
    renderer = ffi.from_handle(lib.misaka_get_renderer(data))
    inline_render = int(inline_render)
    result = renderer.doc_footer(inline_render)
    if result:
        lib.hoedown_buffer_puts(ob, result.encode('utf-8'))


python_callbacks = {
    # block level callbacks - NULL skips the block
    'blockcode':    lib._misaka_blockcode,
    'blockquote':   lib._misaka_blockquote,
    'header':       lib._misaka_header,
    'hrule':        lib._misaka_hrule,
    'list':         lib._misaka_list,
    'listitem':     lib._misaka_listitem,
    'paragraph':    lib._misaka_paragraph,
    'table':        lib._misaka_table,
    'table_header': lib._misaka_table_header,
    'table_body':   lib._misaka_table_body,
    'table_row':    lib._misaka_table_row,
    'table_cell':   lib._misaka_table_cell,
    'footnotes':    lib._misaka_footnotes,
    'footnote_def': lib._misaka_footnote_def,
    'blockhtml':    lib._misaka_blockhtml,

    # span level callbacks - NULL or return 0 prints the span verbatim
    'autolink':        lib._misaka_autolink,
    'codespan':        lib._misaka_codespan,
    'double_emphasis': lib._misaka_double_emphasis,
    'emphasis':        lib._misaka_emphasis,
    'underline':       lib._misaka_underline,
    'highlight':       lib._misaka_highlight,
    'quote':           lib._misaka_quote,
    'image':           lib._misaka_image,
    'linebreak':       lib._misaka_linebreak,
    'link':            lib._misaka_link,
    'triple_emphasis': lib._misaka_triple_emphasis,
    'strikethrough':   lib._misaka_strikethrough,
    'superscript':     lib._misaka_superscript,
    'footnote_ref':    lib._misaka_footnote_ref,
    'math':            lib._misaka_math,
    'raw_html':        lib._misaka_raw_html,

    # low level callbacks - NULL copies input directly into the output
    'entity':      lib._misaka_entity,
    'normal_text': lib._misaka_normal_text,

    # miscellaneous callbacks
    'doc_header': lib._misaka_doc_header,
    'doc_footer': lib._misaka_doc_footer,
}
