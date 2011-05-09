#include <Python.h>
#include <string.h>

#include "upskirt/markdown.h"
#include "upskirt/html.h"


/* The module doc strings */
PyDoc_STRVAR(pantyshot__doc__, "Pantyshot is a Python binding for Upskirt!");
PyDoc_STRVAR(pantyshot_markdown__doc__, "Render Markdown text into HTML.");


static PyObject *
pantyshot_markdown(PyObject *self, PyObject *args, PyObject *kwargs)
{
    struct buf *ib, *ob;
    struct mkd_renderer renderer;
    static char *kwlist[] = {"text", "extensions", "render_flags"};
    const char *text;
    unsigned int extensions = 0, render_flags = 0;
    PyObject *html;

    /* Parse arguments */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|ii", kwlist,
        &text, &extensions, &render_flags))
        return NULL;

    /* Input buffer */
    ib = bufnew(1);
    bufputs(ib, text);

    /* Output buffer */
    ob = bufnew(ib->size * 1.2);

    /* Parse Markdown */
    upshtml_renderer(&renderer, render_flags);
    ups_markdown(ob, ib, &renderer, extensions);
    upshtml_free_renderer(&renderer);

    /* Append a null terminator to the output buffer and make a Python string */
    bufnullterm(ob);
    html = Py_BuildValue("s", ob->data);

    /* Cleanup */
    bufrelease(ib);
    bufrelease(ob);

    return html;
}


static PyMethodDef PantyshotMethods[] = {
    {"markdown",  (PyCFunction) pantyshot_markdown, METH_VARARGS | METH_KEYWORDS,
        pantyshot_markdown__doc__},
    {NULL, NULL, 0, NULL} /* Sentinel */
};


PyMODINIT_FUNC
initpantyshot(void)
{
    PyObject *module;

    /* The module */
    module = Py_InitModule3("pantyshot", PantyshotMethods, pantyshot__doc__);
    if (module == NULL)
        return;

    /* Version */
    PyModule_AddStringConstant(module, "__version__", "0.2.0");

    /* Markdown extensions */
    PyModule_AddIntConstant(module, "EXT_NO_INTRA_EMPHASIS", MKDEXT_NO_INTRA_EMPHASIS);
    PyModule_AddIntConstant(module, "EXT_TABLES", MKDEXT_TABLES);
    PyModule_AddIntConstant(module, "EXT_FENCED_CODE", MKDEXT_FENCED_CODE);
    PyModule_AddIntConstant(module, "EXT_AUTOLINK", MKDEXT_AUTOLINK);
    PyModule_AddIntConstant(module, "EXT_STRIKETHROUGH", MKDEXT_STRIKETHROUGH);
    PyModule_AddIntConstant(module, "EXT_LAX_HTML_BLOCKS", MKDEXT_LAX_HTML_BLOCKS);
    PyModule_AddIntConstant(module, "EXT_SPACE_HEADERS", MKDEXT_SPACE_HEADERS);

    /* XHTML Render flags */
    PyModule_AddIntConstant(module, "HTML_SKIP_HTML", HTML_SKIP_HTML);
    PyModule_AddIntConstant(module, "HTML_SKIP_STYLE", HTML_SKIP_STYLE);
    PyModule_AddIntConstant(module, "HTML_SKIP_IMAGES", HTML_SKIP_IMAGES);
    PyModule_AddIntConstant(module, "HTML_SKIP_LINKS", HTML_SKIP_LINKS);
    PyModule_AddIntConstant(module, "HTML_EXPAND_TABS", HTML_EXPAND_TABS);
    PyModule_AddIntConstant(module, "HTML_SAFELINK", HTML_SAFELINK);
    PyModule_AddIntConstant(module, "HTML_TOC", HTML_TOC);
    PyModule_AddIntConstant(module, "HTML_HARD_WRAP", HTML_HARD_WRAP);
    PyModule_AddIntConstant(module, "HTML_GITHUB_BLOCKCODE", HTML_GITHUB_BLOCKCODE);
    PyModule_AddIntConstant(module, "HTML_USE_XHTML", HTML_USE_XHTML);
}
