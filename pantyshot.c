#include <Python.h>
#include <string.h>

#include "upskirt/markdown.h"
#include "upskirt/xhtml.h"


/* The module doc string */
PyDoc_STRVAR(pantyshot__doc__, "Pantyshot is a Python binding for Upskirt!");
PyDoc_STRVAR(pantyshot_render__doc__, "Render Markdown text into HTML.");


static PyObject *
pantyshot_render(PyObject *self, PyObject *args)
{
    struct buf *ib, *ob;
    struct mkd_renderer renderer;
    const char *input_text;
    const char *output_text;
    char test_str;

    if (!PyArg_ParseTuple(args, "s", &input_text))
        return NULL;

    /* Input buffer */
    ib = bufnew(128);
    bufputs(ib, input_text);

    /* Output buffer */
    ob = bufnew(128);
    bufgrow(ob, strlen(input_text) * 1.2f);

    /* Parse Markdown */
    ups_xhtml_renderer(&renderer, 0);
    ups_markdown(ob, ib, &renderer, 0xFF);
    ups_free_renderer(&renderer);

    output_text = strdup(ob->data);

    /* Cleanup */
    bufrelease(ib);
    bufrelease(ob);

    return Py_BuildValue("s", output_text);
}


static PyMethodDef PantyshotMethods[] = {
    {"render",  pantyshot_render, METH_VARARGS, pantyshot_render__doc__},
    {NULL, NULL, 0, NULL} /* Sentinel */
};


PyMODINIT_FUNC
initpantyshot(void)
{
    PyObject *m;

    m = Py_InitModule3("pantyshot", PantyshotMethods, pantyshot__doc__);
    if (m == NULL)
        return;
}