#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sundown/html.h"


struct renderopt {
    struct html_renderopt html;
    void *self;
};


/* Block level
   ----------- */


void rndr_blockcode(
    struct buf *ob,
    const struct buf *text,
    const struct buf *lang,
    void *opaque);

void rndr_blockquote(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

void rndr_raw_block(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

void rndr_header(
    struct buf *ob,
    const struct buf *text,
    int level,
    void *opaque);

void rndr_hrule (
    struct buf *ob,
    void *opaque);

void rndr_list(
    struct buf *ob,
    const struct buf *text,
    int flags,
    void *opaque);

void rndr_listitem(
    struct buf *ob,
    const struct buf *text,
    int flags,
    void *opaque);

void rndr_paragraph(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

void rndr_table(
    struct buf *ob,
    const struct buf *header,
    const struct buf *body,
    void *opaque);

void rndr_tablerow(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

void rndr_tablecell(
    struct buf *ob,
    const struct buf *text,
    int align,
    void *opaque);


/* Span level
   ---------- */


int rndr_autolink(
    struct buf *ob,
    const struct buf *link,
    enum mkd_autolink type,
    void *opaque);

int rndr_codespan(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

int rndr_double_emphasis(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

int rndr_emphasis(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

int rndr_image(
    struct buf *ob,
    const struct buf *link,
    const struct buf *title,
    const struct buf *alt,
    void *opaque);

int rndr_linebreak(
    struct buf *ob, void *opaque);

int rndr_link(
    struct buf *ob,
    const struct buf *link,
    const struct buf *title,
    const struct buf *content,
    void *opaque);

int rndr_raw_html(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

int rndr_triple_emphasis(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

int rndr_strikethrough(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

int rndr_superscript(
    struct buf *ob,
    const struct buf *text,
    void *opaque);


/* Direct writes
   ------------- */


void rndr_entity(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

void rndr_normal_text(
    struct buf *ob,
    const struct buf *text,
    void *opaque);

void rndr_doc_header(
    struct buf *ob,
    void *opaque);

void rndr_doc_footer(
    struct buf *ob,
    void *opaque);


/* Lists
   ----- */


static struct sd_callbacks callback_funcs = {
    rndr_blockcode,
    rndr_blockquote,
    rndr_raw_block,
    rndr_header,
    rndr_hrule,
    rndr_list,
    rndr_listitem,
    rndr_paragraph,
    rndr_table,
    rndr_tablerow,
    rndr_tablecell,

    rndr_autolink,
    rndr_codespan,
    rndr_double_emphasis,
    rndr_emphasis,
    rndr_image,
    rndr_linebreak,
    rndr_link,
    rndr_raw_html,
    rndr_triple_emphasis,
    rndr_strikethrough,
    rndr_superscript,

    rndr_entity,
    rndr_normal_text,

    rndr_doc_header,
    rndr_doc_footer,
};


static const char *method_names[] = {
    "block_code",
    "block_quote",
    "block_html",
    "header",
    "hrule",
    "list",
    "list_item",
    "paragraph",
    "table",
    "table_row",
    "table_cell",

    "autolink",
    "codespan",
    "double_emphasis",
    "emphasis",
    "image",
    "linebreak",
    "link",
    "raw_html",
    "triple_emphasis",
    "strikethrough",
    "superscript",

    "entity",
    "normal_text",

    "doc_header",
    "doc_footer"
};


static const size_t method_count = sizeof(
    method_names)/sizeof(char *);
