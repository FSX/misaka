#include <Python.h>
#include <string.h>

#include "upskirt/markdown.h"
#include "upskirt/html.h"


/* An extra flag to enabled Smartypants */
unsigned int HTML_SMARTYPANTS = (1 << 12);


/* The module doc strings */
PyDoc_STRVAR(pantyshot_module__doc__, "Pantyshot is a Python binding for Upskirt!");
PyDoc_STRVAR(pantyshot_markdown__doc__, "Render Markdown text into HTML.");
PyDoc_STRVAR(pantyshot_html__doc__, "Render Markdown text into HTML.");
PyDoc_STRVAR(pantyshot_toc__doc__, "Generate a table of contents.");


static PyObject *
pantyshot_render(const char *text, unsigned int extensions,
                 unsigned int render_flags, char toc_only)
{
    struct buf *ib, *ob;
    struct mkd_renderer renderer;

    /* Input buffer */
    ib = bufnew(1);
    bufputs(ib, text);

    /* Output buffer */
    ob = bufnew(ib->size * 1.2);

    /* Parse Markdown */
    if (toc_only != -1) {
        upshtml_toc_renderer(&renderer);
    } else{
        upshtml_renderer(&renderer, render_flags);
    }

    ups_markdown(ob, ib, &renderer, extensions);
    upshtml_free_renderer(&renderer);

    /* Smartypants actions */
    if (render_flags & HTML_SMARTYPANTS)
    {
        struct buf *sb = bufnew(1);
        upshtml_smartypants(sb, ob);
        ob = bufdup(sb, sb->size); /* Duplicate Smartypants buffer to output buffer */
        bufrelease(sb); /* Cleanup Smartypants buffer */
    }

    /* Append a null terminator to the output buffer and make a Python string */
    bufnullterm(ob);
    PyObject *html = Py_BuildValue("s", ob->data);

    /* Cleanup */
    bufrelease(ib);
    bufrelease(ob);

    return html;
}


static PyObject *
pantyshot_html(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"text", "extensions", "render_flags"};
    unsigned int extensions = 0, render_flags = 0;
    const char *text;

    /* Parse arguments */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|ii", kwlist,
        &text, &extensions, &render_flags))
        return NULL;

    return pantyshot_render(text, extensions, render_flags, -1);
}


static PyObject *
pantyshot_toc(PyObject *self, PyObject *args)
{
    const char *text;

    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "s", &text))
        return NULL;

    return pantyshot_render(text, 0, 0, 1);
}


static PyMethodDef PantyshotMethods[] = {
    {"html", (PyCFunction) pantyshot_html, METH_VARARGS | METH_KEYWORDS, pantyshot_html__doc__},
    {"toc", (PyCFunction) pantyshot_toc, METH_VARARGS,pantyshot_toc__doc__},
    {NULL, NULL, 0, NULL} /* Sentinel */
};


PyMODINIT_FUNC
initpantyshot(void)
{
    /* The module */
    PyObject *module = Py_InitModule3("pantyshot", PantyshotMethods,
        pantyshot_module__doc__);
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
    PyModule_AddIntConstant(module, "HTML_SMARTYPANTS", HTML_SMARTYPANTS);
}
