# -*- coding: utf-8 -*-

import cffi


# Block-level extensions
EXT_TABLES = (1 << 0)
EXT_FENCED_CODE = (1 << 1)
EXT_FOOTNOTES = (1 << 2)

# Span-level extensions
EXT_AUTOLINK = (1 << 3)
EXT_STRIKETHROUGH = (1 << 4)
EXT_UNDERLINE = (1 << 5)
EXT_HIGHLIGHT = (1 << 6)
EXT_QUOTE = (1 << 7)
EXT_SUPERSCRIPT = (1 << 8)
EXT_MATH = (1 << 9)

# Other flags
EXT_NO_INTRA_EMPHASIS = (1 << 11)
EXT_SPACE_HEADERS = (1 << 12)
EXT_MATH_EXPLICIT = (1 << 13)

# Negative flags
EXT_DISABLE_INDENTED_CODE = (1 << 14)

# List flags
LIST_ORDERED = (1 << 0)
LI_BLOCK = (1 << 1)  # <li> containing block data

# Table flags
TABLE_ALIGN_LEFT = 1
TABLE_ALIGN_RIGHT = 2
TABLE_ALIGN_CENTER = 3
TABLE_ALIGNMASK = 3
TABLE_HEADER = 4

# HTML flags
HTML_SKIP_HTML = (1 << 0)
HTML_ESCAPE = (1 << 1)
HTML_HARD_WRAP = (1 << 2)
HTML_USE_XHTML = (1 << 3)

# Autolink types
AUTOLINK_NONE = 1  # Used internally when it is not an autolink
AUTOLINK_NORMAL = 2  # Normal http/http/ftp/mailto/etc link
AUTOLINK_EMAIL = 3  # E-mail link without explit mailto:


ffi = cffi.FFI()

ffi.set_source(
    'misaka._hoedown',
    """\
#include "hoedown/buffer.h"
#include "hoedown/document.h"
#include "hoedown/escape.h"
#include "hoedown/html.h"
#include "extra.h"
""",
    sources=(
        'misaka/hoedown/version.c',
        'misaka/hoedown/stack.c',
        'misaka/hoedown/html_smartypants.c',
        'misaka/hoedown/html_blocks.c',
        'misaka/hoedown/html.c',
        'misaka/hoedown/escape.c',
        'misaka/hoedown/document.c',
        'misaka/hoedown/buffer.c',
        'misaka/hoedown/autolink.c',
        'misaka/extra.c',
    ),
    include_dirs=('misaka',))


# NOTE: The constants are refined here, because CFFI
# doesn't parse the bitwise left-shift (<<).
ffi.cdef("""\
// --------------------------
// --- hoedown/document.h ---
// --------------------------

typedef enum hoedown_extensions {{
    /* block-level extensions */
    HOEDOWN_EXT_TABLES = {0},
    HOEDOWN_EXT_FENCED_CODE = {1},
    HOEDOWN_EXT_FOOTNOTES = {2},
    HOEDOWN_EXT_AUTOLINK = {3},
    HOEDOWN_EXT_STRIKETHROUGH = {4},
    HOEDOWN_EXT_UNDERLINE = {5},
    HOEDOWN_EXT_HIGHLIGHT = {6},
    HOEDOWN_EXT_QUOTE = {7},
    HOEDOWN_EXT_SUPERSCRIPT = {8},
    HOEDOWN_EXT_MATH = {9},
    HOEDOWN_EXT_NO_INTRA_EMPHASIS = {10},
    HOEDOWN_EXT_SPACE_HEADERS = {11},
    HOEDOWN_EXT_MATH_EXPLICIT = {12},
    HOEDOWN_EXT_DISABLE_INDENTED_CODE = {13}
}} hoedown_extensions;

typedef enum hoedown_list_flags {{
    HOEDOWN_LIST_ORDERED = {14},
    HOEDOWN_LI_BLOCK = {15}
}} hoedown_list_flags;

typedef enum hoedown_table_flags {{
    HOEDOWN_TABLE_ALIGN_LEFT = {16},
    HOEDOWN_TABLE_ALIGN_RIGHT = {17},
    HOEDOWN_TABLE_ALIGN_CENTER = {18},
    HOEDOWN_TABLE_ALIGNMASK = {19},
    HOEDOWN_TABLE_HEADER = {20}
}} hoedown_table_flags;

// ----------------------
// --- hoedown/html.h ---
// ----------------------

typedef enum hoedown_html_flags {{
    HOEDOWN_HTML_SKIP_HTML = {21},
    HOEDOWN_HTML_ESCAPE = {22},
    HOEDOWN_HTML_HARD_WRAP = {23},
    HOEDOWN_HTML_USE_XHTML = {24}
}} hoedown_html_flags;
""".format(
    EXT_TABLES,
    EXT_FENCED_CODE,
    EXT_FOOTNOTES,
    EXT_AUTOLINK,
    EXT_STRIKETHROUGH,
    EXT_UNDERLINE,
    EXT_HIGHLIGHT,
    EXT_QUOTE,
    EXT_SUPERSCRIPT,
    EXT_MATH,
    EXT_NO_INTRA_EMPHASIS,
    EXT_SPACE_HEADERS,
    EXT_MATH_EXPLICIT,
    EXT_DISABLE_INDENTED_CODE,
    LIST_ORDERED,
    LI_BLOCK,
    TABLE_ALIGN_LEFT,
    TABLE_ALIGN_RIGHT,
    TABLE_ALIGN_CENTER,
    TABLE_ALIGNMASK,
    TABLE_HEADER,
    HTML_SKIP_HTML,
    HTML_ESCAPE,
    HTML_HARD_WRAP,
    HTML_USE_XHTML))


ffi.cdef("""\
// ------------------------
// --- hoedown/buffer.h ---
// ------------------------

typedef void *(*hoedown_realloc_callback)(void *, size_t);
typedef void (*hoedown_free_callback)(void *);

struct hoedown_buffer {
    uint8_t *data;  /* actual character data */
    size_t size;    /* size of the string */
    size_t asize;   /* allocated size (0 = volatile buffer) */
    size_t unit;    /* reallocation unit size (0 = read-only buffer) */

    hoedown_realloc_callback data_realloc;
    hoedown_free_callback data_free;
    hoedown_free_callback buffer_free;
};

typedef struct hoedown_buffer hoedown_buffer;

void *hoedown_malloc(size_t size);
hoedown_buffer *hoedown_buffer_new(size_t unit);
void hoedown_buffer_grow(hoedown_buffer *buf, size_t neosz);
void hoedown_buffer_puts(hoedown_buffer *buf, const char *str);
void hoedown_buffer_free(hoedown_buffer *buf);

// --------------------------
// --- hoedown/document.h ---
// --------------------------

// NOTE: See earlier ff.cdef() for document.h's constants.

typedef enum hoedown_autolink_type {
    HOEDOWN_AUTOLINK_NONE,      /* used internally when it is not an autolink*/
    HOEDOWN_AUTOLINK_NORMAL,    /* normal http/http/ftp/mailto/etc link */
    HOEDOWN_AUTOLINK_EMAIL      /* e-mail link without explit mailto: */
} hoedown_autolink_type;

struct hoedown_document;
typedef struct hoedown_document hoedown_document;

struct hoedown_renderer_data {
    void *opaque;
};
typedef struct hoedown_renderer_data hoedown_renderer_data;

/* hoedown_renderer - functions for rendering parsed data */
struct hoedown_renderer {
    /* state object */
    void *opaque;

    /* block level callbacks - NULL skips the block */
    void (*blockcode)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_buffer *lang, const hoedown_renderer_data *data);
    void (*blockquote)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    void (*header)(hoedown_buffer *ob, const hoedown_buffer *content, int level, const hoedown_renderer_data *data);
    void (*hrule)(hoedown_buffer *ob, const hoedown_renderer_data *data);
    void (*list)(hoedown_buffer *ob, const hoedown_buffer *content, hoedown_list_flags flags, const hoedown_renderer_data *data);
    void (*listitem)(hoedown_buffer *ob, const hoedown_buffer *content, hoedown_list_flags flags, const hoedown_renderer_data *data);
    void (*paragraph)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    void (*table)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    void (*table_header)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    void (*table_body)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    void (*table_row)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    void (*table_cell)(hoedown_buffer *ob, const hoedown_buffer *content, hoedown_table_flags flags, const hoedown_renderer_data *data);
    void (*footnotes)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    void (*footnote_def)(hoedown_buffer *ob, const hoedown_buffer *content, unsigned int num, const hoedown_renderer_data *data);
    void (*blockhtml)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data);

    /* span level callbacks - NULL or return 0 prints the span verbatim */
    int (*autolink)(hoedown_buffer *ob, const hoedown_buffer *link, hoedown_autolink_type type, const hoedown_renderer_data *data);
    int (*codespan)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data);
    int (*double_emphasis)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    int (*emphasis)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    int (*underline)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    int (*highlight)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    int (*quote)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    int (*image)(hoedown_buffer *ob, const hoedown_buffer *link, const hoedown_buffer *title, const hoedown_buffer *alt, const hoedown_renderer_data *data);
    int (*linebreak)(hoedown_buffer *ob, const hoedown_renderer_data *data);
    int (*link)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_buffer *link, const hoedown_buffer *title, const hoedown_renderer_data *data);
    int (*triple_emphasis)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    int (*strikethrough)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    int (*superscript)(hoedown_buffer *ob, const hoedown_buffer *content, const hoedown_renderer_data *data);
    int (*footnote_ref)(hoedown_buffer *ob, unsigned int num, const hoedown_renderer_data *data);
    int (*math)(hoedown_buffer *ob, const hoedown_buffer *text, int displaymode, const hoedown_renderer_data *data);
    int (*raw_html)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data);

    /* low level callbacks - NULL copies input directly into the output */
    void (*entity)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data);
    void (*normal_text)(hoedown_buffer *ob, const hoedown_buffer *text, const hoedown_renderer_data *data);

    /* miscellaneous callbacks */
    void (*doc_header)(hoedown_buffer *ob, int inline_render, const hoedown_renderer_data *data);
    void (*doc_footer)(hoedown_buffer *ob, int inline_render, const hoedown_renderer_data *data);
};
typedef struct hoedown_renderer hoedown_renderer;

hoedown_document *hoedown_document_new(
    const hoedown_renderer *renderer,
    hoedown_extensions extensions,
    size_t max_nesting
);

void hoedown_document_render(hoedown_document *doc, hoedown_buffer *ob, const uint8_t *data, size_t size);
void hoedown_document_free(hoedown_document *doc);

// ------------------------
// --- hoedown/escape.h ---
// ------------------------

void hoedown_escape_html(hoedown_buffer *ob, const uint8_t *data, size_t size, int secure);

// ----------------------
// --- hoedown/html.h ---
// ----------------------

// NOTE: See earlier ff.cdef() for html.h's constants.

typedef enum hoedown_html_tag {
    HOEDOWN_HTML_TAG_NONE = 0,
    HOEDOWN_HTML_TAG_OPEN,
    HOEDOWN_HTML_TAG_CLOSE
} hoedown_html_tag;

hoedown_renderer *hoedown_html_renderer_new(
    hoedown_html_flags render_flags,
    int nesting_level
);
hoedown_renderer *hoedown_html_toc_renderer_new(
    int nesting_level
);
void hoedown_html_renderer_free(hoedown_renderer *renderer);
void hoedown_html_smartypants(hoedown_buffer *ob, const uint8_t *data, size_t size);

// ---------------
// --- extra.h ---
// ---------------

void *misaka_get_renderer(const hoedown_renderer_data *data);
""")


if __name__ == '__main__':
    ffi.compile()
