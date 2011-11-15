#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sundown/markdown.h"
#include "sundown/buffer.h"

#include "wrapper.h"


#define SPAN_PROCESS_OUTPUT(ret) {\
    if (ret == NULL || ret == Py_None || !PyString_Check(ret))\
        return 0;\
    bufputs(ob, PyString_AsString(ret));\
    return 1;\
}


#define BLOCK_PROCESS_OUTPUT(ret) {\
    if (ret == NULL || ret == Py_None || !PyString_Check(ret))\
        return;\
    bufputs(ob, PyString_AsString(ret));\
}


/* Block level
   ----------- */


void
rndr_blockcode(struct buf *ob, const struct buf *text, const struct buf *lang, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "block_code", "ss",
        bufcstr((struct buf *) text),
        bufcstr((struct buf *) lang)
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_blockquote(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "block_quote", "s",
        bufcstr((struct buf *) text)
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_raw_block(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "block_html", "s",
        bufcstr((struct buf *) text)
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_header(struct buf *ob, const struct buf *text, int level, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "header", "si",
        bufcstr((struct buf *) text),
        level
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_hrule(struct buf *ob, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "hrule", NULL);
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_list(struct buf *ob, const struct buf *text, int flags, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "list", "ss",
        bufcstr((struct buf *) text),
        (flags & MKD_LIST_ORDERED ? "ordered" : "unordered")
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_listitem(struct buf *ob, const struct buf *text, int flags, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "list_item", "ss",
        bufcstr((struct buf *) text),
        (flags & MKD_LIST_ORDERED ? "ordered" : "unordered")
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_paragraph(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "paragraph", "s",
        bufcstr((struct buf *) text)
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_table(struct buf *ob, const struct buf *header, const struct buf *body, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "rndr_table", "ss",
        bufcstr((struct buf *) header),
        bufcstr((struct buf *) body)
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_tablerow(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "table_row", "s",
        bufcstr((struct buf *) text)
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_tablecell(struct buf *ob, const struct buf *text, int align, void *opaque)
{
    char *str_align;

    switch (align) {
    case MKD_TABLE_ALIGN_L:
        str_align = "left";
        break;

    case MKD_TABLE_ALIGN_R:
        str_align = "right";
        break;

    case MKD_TABLE_ALIGN_CENTER:
        str_align = "center";
        break;

    default:
        str_align = NULL;
        break;
    }

    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "table_cell", "ss",
        bufcstr((struct buf *) text),
        str_align
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


/* Span level
   ---------- */


int
rndr_autolink(struct buf *ob, const struct buf *link, enum mkd_autolink type, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "autolink", "ss",
        bufcstr((struct buf *) link),
        (type == MKDA_NORMAL ? "url" : "email")
    );
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_codespan(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "codespan", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_double_emphasis(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "double_emphasis", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_emphasis(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "emphasis", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_image(struct buf *ob, const struct buf *link, const struct buf *title, const struct buf *alt, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "image", "sss",
        bufcstr((struct buf *) link),
        bufcstr((struct buf *) title),
        bufcstr((struct buf *) alt)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_linebreak(struct buf *ob, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "linebreak", NULL);
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_link(struct buf *ob, const struct buf *link, const struct buf *title, const struct buf *content, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "link", "sss",
        bufcstr((struct buf *) link),
        bufcstr((struct buf *) title),
        bufcstr((struct buf *) content)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_raw_html(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "raw_html", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_triple_emphasis(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "triple_emphasis", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_strikethrough(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "strikethrough", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


int
rndr_superscript(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "superscript", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


/* Direct writes
   ------------- */


void
rndr_entity(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "entity", "s",
        bufcstr((struct buf *) text)
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_normal_text(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "normal_text", "s",
        bufcstr((struct buf *) text)
    );
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_doc_header(struct buf *ob, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "doc_header", NULL);
    BLOCK_PROCESS_OUTPUT(ret);
}


void
rndr_doc_footer(struct buf *ob, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "doc_footer", NULL);
    BLOCK_PROCESS_OUTPUT(ret);
}
