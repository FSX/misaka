#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sundown/markdown.h"
#include "sundown/buffer.h"

#include "wrapper.h"


#define SPAN_PROCESS_OUTPUT(ret) {\
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
    PROCESS_BLOCK("list", PY_STR(text), PY_INT(flags), NULL);
}


static void
rndr_listitem(struct buf *ob, const struct buf *text, int flags, void *opaque)
{
    PROCESS_BLOCK("list_item", PY_STR(text), PY_INT(flags), NULL);
}


static void
rndr_paragraph(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_BLOCK("paragraph", PY_STR(text), NULL);
}


static void
rndr_table(struct buf *ob, const struct buf *header, const struct buf *body, void *opaque)
{
    PROCESS_BLOCK("rndr_table", PY_STR(header), PY_STR(body), NULL);
}


static void
rndr_tablerow(struct buf *ob, const struct buf *text, void *opaque)
{
    PROCESS_BLOCK("table_row", PY_STR(text), NULL);
}


static void
rndr_tablecell(struct buf *ob, const struct buf *text, int align, void *opaque)
{
    // char *str_align;

    // switch (align) {
    // case MKD_TABLE_ALIGN_L:
    //     str_align = "left";
    //     break;

    // case MKD_TABLE_ALIGN_R:
    //     str_align = "right";
    //     break;

    // case MKD_TABLE_ALIGN_CENTER:
    //     str_align = "center";
    //     break;

    // default:
    //     str_align = NULL;
    //     break;
    // }

    PROCESS_BLOCK("table_row", PY_STR(text), PY_INT(align), NULL);
}


/* Span level
   ---------- */


static int
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


static int
rndr_codespan(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "codespan", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


static int
rndr_double_emphasis(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "double_emphasis", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


static int
rndr_emphasis(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "emphasis", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


static int
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


static int
rndr_linebreak(struct buf *ob, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "linebreak", NULL);
    SPAN_PROCESS_OUTPUT(ret);
}


static int
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


static int
rndr_raw_html(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "raw_html", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


static int
rndr_triple_emphasis(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "triple_emphasis", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


static int
rndr_strikethrough(struct buf *ob, const struct buf *text, void *opaque)
{
    struct renderopt *opt = opaque;
    PyObject *ret = PyObject_CallMethod(
        (PyObject *) opt->self, "strikethrough", "s",
        bufcstr((struct buf *) text)
    );
    SPAN_PROCESS_OUTPUT(ret);
}


static int
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
