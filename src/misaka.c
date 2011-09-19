#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include "sundown/markdown.h"
#include "sundown/html.h"
#include "sundown/buffer.h"


/* An extra flag to enabled Smartypants */
static const unsigned int HTML_SMARTYPANTS = (1 << 9);

/* Only render a table of contents tree */
static const unsigned int HTML_TOC_TREE = (1 << 10);


/* The module doc strings */
PyDoc_STRVAR(misaka_module__doc__, "Misaka is a Python binding for Sundown!");
PyDoc_STRVAR(misaka_html__doc__, "Render Markdown text into HTML.");


/* Renderer class
----------------------------------------------------------------------------- */

typedef struct {
    PyObject_HEAD
    unsigned int render_flags;
} Renderer;


static void
Renderer_dealloc(Renderer* self)
{
    self->ob_type->tp_free((PyObject*)self);
}


static PyObject *
Renderer_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Renderer *self;

    self = (Renderer *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->render_flags = 0;
    }

    return (PyObject *)self;
}


static int
Renderer_init(Renderer *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"first", "last", "number", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds,
        "|i", kwlist, &self->render_flags)) {
        return -1;
    }

    return 0;
}


static PyMemberDef Renderer_members[] = {
    {"render_flags", T_INT, offsetof(Renderer, render_flags), 0, NULL},
    {NULL}  /* Sentinel */
};


static PyMethodDef Renderer_methods[] = {
    {NULL}  /* Sentinel */
};


static PyTypeObject RendererType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "misaka.Renderer",         /*tp_name*/
    sizeof(Renderer),          /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)Renderer_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
    0,                         /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    Renderer_methods,          /* tp_methods */
    Renderer_members,          /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc)Renderer_init,   /* tp_init */
    0,                         /* tp_alloc */
    Renderer_new,              /* tp_new */
};


/* Simple Markdown to HTML function
----------------------------------------------------------------------------- */

static PyObject *
misaka_html(PyObject *self, PyObject *args, PyObject *kwargs)
{
    struct sd_callbacks callbacks;
    struct html_renderopt options;
    struct sd_markdown *markdown;
    static char *kwlist[] = {"text", "extensions", "render_flags", NULL};

    struct buf ib, *ob;
    unsigned int extensions = 0, render_flags = 0;

    PyObject *py_result;

    memset(&ib, 0x0, sizeof(struct buf));

    /* Parse arguments */
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s#|ii", kwlist,
        &ib.data, &ib.size, &extensions, &render_flags)) {
        return NULL;
    }

    /* Output buffer */
    ob = bufnew(128);
    bufgrow(ob, ib.size * 1.4f);

    /* Parse Markdown */
    if (render_flags & HTML_TOC_TREE) {
        sdhtml_toc_renderer(&callbacks, &options);
    } else {
        sdhtml_renderer(&callbacks, &options, render_flags);
    }

    markdown = sd_markdown_new(extensions, 16, &callbacks, &options);
    sd_markdown_render(ob, ib.data, ib.size, markdown);
    sd_markdown_free(markdown);

    /* Smartypants actions */
    if (render_flags & HTML_SMARTYPANTS) {
        struct buf *sb = bufnew(128);
        sdhtml_smartypants(sb, ob->data, ob->size);
        bufrelease(ob);
        ob = sb;
    }

    /* Make a Python string */
    py_result = Py_BuildValue("s#", ob->data, (int)ob->size);

    /* Cleanup */
    bufrelease(ob);
    return py_result;
}


/* Misaka module
----------------------------------------------------------------------------- */

static PyMethodDef misaka_methods[] = {
    {"html", (PyCFunction) misaka_html, METH_VARARGS | METH_KEYWORDS, misaka_html__doc__},
    {NULL, NULL, 0, NULL} /* Sentinel */
};


#if PY_MAJOR_VERSION >= 3
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "misaka",
        misaka_module__doc__,
        -1,
        misaka_methods,
        NULL,
        NULL,
        NULL,
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
    RendererType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&RendererType) < 0)
        return;

    #if PY_MAJOR_VERSION >= 3
        PyObject *module = PyModule_Create(&moduledef);
    #else
        PyObject *module = Py_InitModule3("misaka", misaka_methods,
            misaka_module__doc__);
    #endif

    if (module == NULL) {
        INITERROR;
    }

    /* Version */
    PyModule_AddStringConstant(module, "__version__", "0.4.3");

    /* Markdown extensions */
    PyModule_AddIntConstant(module, "EXT_NO_INTRA_EMPHASIS", MKDEXT_NO_INTRA_EMPHASIS);
    PyModule_AddIntConstant(module, "EXT_TABLES", MKDEXT_TABLES);
    PyModule_AddIntConstant(module, "EXT_FENCED_CODE", MKDEXT_FENCED_CODE);
    PyModule_AddIntConstant(module, "EXT_AUTOLINK", MKDEXT_AUTOLINK);
    PyModule_AddIntConstant(module, "EXT_STRIKETHROUGH", MKDEXT_STRIKETHROUGH);
    PyModule_AddIntConstant(module, "EXT_LAX_HTML_BLOCKS", MKDEXT_LAX_HTML_BLOCKS);
    PyModule_AddIntConstant(module, "EXT_SPACE_HEADERS", MKDEXT_SPACE_HEADERS);
    PyModule_AddIntConstant(module, "EXT_SUPERSCRIPT", MKDEXT_SUPERSCRIPT);

    /* HTML Render flags */
    PyModule_AddIntConstant(module, "HTML_SKIP_HTML", HTML_SKIP_HTML);
    PyModule_AddIntConstant(module, "HTML_SKIP_STYLE", HTML_SKIP_STYLE);
    PyModule_AddIntConstant(module, "HTML_SKIP_IMAGES", HTML_SKIP_IMAGES);
    PyModule_AddIntConstant(module, "HTML_SKIP_LINKS", HTML_SKIP_LINKS);
    PyModule_AddIntConstant(module, "HTML_EXPAND_TABS", HTML_EXPAND_TABS);
    PyModule_AddIntConstant(module, "HTML_SAFELINK", HTML_SAFELINK);
    PyModule_AddIntConstant(module, "HTML_TOC", HTML_TOC);
    PyModule_AddIntConstant(module, "HTML_HARD_WRAP", HTML_HARD_WRAP);
    PyModule_AddIntConstant(module, "HTML_USE_XHTML", HTML_USE_XHTML);

    /* Extra HTML render flags - these are not from Sundown */
    PyModule_AddIntConstant(module, "HTML_SMARTYPANTS", HTML_SMARTYPANTS);
    PyModule_AddIntConstant(module, "HTML_TOC_TREE", HTML_TOC_TREE);

    Py_INCREF(&RendererType);
    PyModule_AddObject(module, "Renderer", (PyObject *)&RendererType);

    #if PY_MAJOR_VERSION >= 3
        return module;
    #endif
}
