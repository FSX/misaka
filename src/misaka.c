#include <Python.h>

#include "sundown/markdown.h"
#include "sundown/html.h"


struct module_state {
    PyObject *error;
};


#if PY_MAJOR_VERSION >= 3
    #define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
    #define GETSTATE(m) (&_state)
    static struct module_state _state;
#endif


/* An extra flag to enabled Smartypants */
unsigned int HTML_SMARTYPANTS = (1 << 12);


/* The module doc strings */
PyDoc_STRVAR(misaka_module__doc__, "Misaka is a Python binding for Sundown!");
PyDoc_STRVAR(misaka_html__doc__, "Render Markdown text into HTML.");
PyDoc_STRVAR(misaka_toc__doc__, "Generate a table of contents.");


static PyObject *
misaka_render(const char *text, unsigned int extensions,
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
        sdhtml_toc_renderer(&renderer);
    } else {
        sdhtml_renderer(&renderer, render_flags);
    }

    sd_markdown(ob, ib, &renderer, extensions);
    sdhtml_free_renderer(&renderer);

    /* Smartypants actions */
    if (render_flags & HTML_SMARTYPANTS)
    {
        struct buf *sb = bufnew(1);
        sdhtml_smartypants(sb, ob);
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
misaka_html(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"text", "extensions", "render_flags", NULL};
    unsigned int extensions = 0, render_flags = 0;
    const char *text;

    /* Parse arguments */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|ii", kwlist,
        &text, &extensions, &render_flags)) {
        return NULL;
    }

    return misaka_render(text, extensions, render_flags, -1);
}


static PyObject *
misaka_toc(PyObject *self, PyObject *args)
{
    const char *text;

    /* Parse arguments */
    if (!PyArg_ParseTuple(args, "s", &text)) {
        return NULL;
    }

    return misaka_render(text, 0, 0, 1);
}


static PyMethodDef misaka_methods[] = {
    {"html", (PyCFunction) misaka_html, METH_VARARGS | METH_KEYWORDS, misaka_html__doc__},
    {"toc", (PyCFunction) misaka_toc, METH_VARARGS, misaka_toc__doc__},
    {NULL, NULL, 0, NULL} /* Sentinel */
};


#if PY_MAJOR_VERSION >= 3
    static int
    misaka_traverse(PyObject *m, visitproc visit, void *arg)
    {
        Py_VISIT(GETSTATE(m)->error);
        return 0;
    }

    static int
    misaka_clear(PyObject *m)
    {
        Py_CLEAR(GETSTATE(m)->error);
        return 0;
    }

    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "misaka",
        misaka_module__doc__,
        sizeof(struct module_state),
        misaka_methods,
        NULL,
        misaka_traverse,
        misaka_clear,
        NULL
    };

    #define INITERROR return NULL

    PyObject *
    PyInit_misaka(void)
#else
    #define INITERROR return

    PyMODINIT_FUNC
    initmisaka(void)
#endif
{
    #if PY_MAJOR_VERSION >= 3
        PyObject *module = PyModule_Create(&moduledef);
    #else
        PyObject *module = Py_InitModule3("misaka", misaka_methods,
            misaka_module__doc__);
    #endif

    if (module == NULL) {
        INITERROR;
    }
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("misaka.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

    /* Version */
    PyModule_AddStringConstant(module, "__version__", "0.3.3");

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

    #if PY_MAJOR_VERSION >= 3
        return module;
    #endif
}
