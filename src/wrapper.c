#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sundown/markdown.h"
#include "sundown/buffer.h"

#include "wrapper.h"


#define PROCESS_SPAN(method_name, ...) {\
    struct renderopt *opt = opaque;\
    PyObject *ret = PyObject_CallMethodObjArgs(\
        (PyObject *) opt->self, Py_BuildValue("s", method_name),\
        __VA_ARGS__);\
    if (ret == NULL || ret == Py_None)\
        return 0;\
    if (PyUnicode_Check(ret)) {\
        PyObject *byte_string = PyUnicode_AsEncodedString(ret, "utf-8", "strict");\
        bufputs(ob, PyBytes_AsString(byte_string));\
    } else {\
        bufputs(ob, PyBytes_AsString(ret));\
    }\
    return 1;\
}


#define PROCESS_BLOCK(method_name, ...) {\
    struct renderopt *opt = opaque;\
    PyObject *ret = PyObject_CallMethodObjArgs(\
        (PyObject *) opt->self, Py_BuildValue("s", method_name),\
        __VA_ARGS__);\
    if (ret == NULL || ret == Py_None)\
        return;\
    if (PyUnicode_Check(ret)) {\
        PyObject *byte_string = PyUnicode_AsEncodedString(ret, "utf-8", "strict");\
        bufputs(ob, PyBytes_AsString(byte_string));\
    } else {\
        bufputs(ob, PyBytes_AsString(ret));\
    }\
}


#define PY_STR(b) (b != NULL ? Py_BuildValue("s#", b->data, (int) b->size) : Py_None)
#define PY_INT(i) PyInt_FromLong(i)


/* Block level
   ----------- */


static void
rndr_blockcode(struct buf *ob, const struct buf *text, const struct buf *lang, void *opaque)
{
    PROCESS_BLOCK("block_code", PY_STR(text), PY_STR(lang), NULL);
}


static void
rndr_blockquote(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_BLOCK("block_quote", PY_STR(text), NULL);
}


static void
rndr_raw_block(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_BLOCK("block_html", PY_STR(text), NULL);
}


static void
rndr_header(struct buf *ob, const struct buf *text, int level, void *opaque)
{
    PROCESS_BLOCK("header", PY_STR(text), PY_INT(level), NULL);
}


static void
rndr_hrule(struct buf *ob, void *opaque)
{
    PROCESS_BLOCK("hrule", NULL);
}


static void
rndr_list(struct buf *ob, const struct buf *text, int flags, void *opaque)
{
    PyObject *is_ordered = Py_False;
    if (flags & MKD_LIST_ORDERED) {
        is_ordered = Py_True;
    }

    PROCESS_BLOCK("list", PY_STR(text), is_ordered, NULL);
}


static void
rndr_listitem(struct buf *ob, const struct buf *text, int flags, void *opaque)
{
    PyObject *is_ordered = Py_False;
    if (flags & MKD_LIST_ORDERED) {
        is_ordered = Py_True;
    }

    PROCESS_BLOCK("list_item", PY_STR(text), is_ordered, NULL);
}


static void
rndr_paragraph(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_BLOCK("paragraph", PY_STR(text), NULL);
}


static void
rndr_table(struct buf *ob, const struct buf *header, const struct buf *body, void *opaque)
{
    PROCESS_BLOCK("table", PY_STR(header), PY_STR(body), NULL);
}


static void
rndr_tablerow(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_BLOCK("table_row", PY_STR(text), NULL);
}


static void
rndr_tablecell(struct buf *ob, const struct buf *text, int flags, void *opaque)
{
    PROCESS_BLOCK("table_cell", PY_STR(text), PY_INT(flags), NULL);
}


/* Span level
   ---------- */


static int
rndr_autolink(struct buf *ob, const struct buf *link, enum mkd_autolink type, void *opaque)
{
    PyObject *is_email = Py_False;
    if (type == MKDA_EMAIL) {
        is_email = Py_True;
    }

    PROCESS_SPAN("autolink", PY_STR(link), is_email, NULL);
}


static int
rndr_codespan(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_SPAN("codespan", PY_STR(text), NULL);
}


static int
rndr_double_emphasis(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_SPAN("double_emphasis", PY_STR(text), NULL);
}


static int
rndr_emphasis(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_SPAN("emphasis", PY_STR(text), NULL);
}


static int
rndr_image(struct buf *ob, const struct buf *link, const struct buf *title, const struct buf *alt, void *opaque)
{
    PROCESS_SPAN("image", PY_STR(link), PY_STR(title), PY_STR(alt), NULL);
}


static int
rndr_linebreak(struct buf *ob, void *opaque)
{
    PROCESS_SPAN("linebreak", NULL);
}


static int
rndr_link(struct buf *ob, const struct buf *link, const struct buf *title, const struct buf *content, void *opaque)
{
    PROCESS_SPAN("link", PY_STR(link), PY_STR(title), PY_STR(content), NULL);
}


static int
rndr_raw_html(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_SPAN("raw_html", PY_STR(text), NULL);
}


static int
rndr_triple_emphasis(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_SPAN("triple_emphasis", PY_STR(text), NULL);
}


static int
rndr_strikethrough(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_SPAN("strikethrough", PY_STR(text), NULL);
}


static int
rndr_superscript(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_SPAN("superscript", PY_STR(text), NULL);
}


/* Direct writes
   ------------- */


static void
rndr_entity(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_BLOCK("entity", PY_STR(text), NULL);
}


static void
rndr_normal_text(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_BLOCK("normal_text", PY_STR(text), NULL);
}


static void
rndr_doc_header(struct buf *ob, void *opaque)
{
    PROCESS_BLOCK("doc_header", NULL);
}


static void
rndr_doc_footer(struct buf *ob, void *opaque)
{
    PROCESS_BLOCK("doc_footer", NULL);
}


struct sd_callbacks callback_funcs = {
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


const char *method_names[] = {
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


const size_t method_count = sizeof(
    method_names)/sizeof(char *);
