#include <Python.h>
#include <string.h>

#include "upskirt/markdown.h"
#include "upskirt/xhtml.h"


/* The module doc string */
PyDoc_STRVAR(pantyshot__doc__, "Pantyshot is a Python binding for Upskirt!");
PyDoc_STRVAR(pantyshot_markdown__doc__, "Render Markdown text into HTML.");


static PyObject *
pantyshot_markdown(PyObject *self, PyObject *args)
{
    struct buf *ib, *ob;
    struct mkd_renderer renderer;
    const char *input_text;
    const char *output_text;

    if (!PyArg_ParseTuple(args, "s", &input_text))
        return NULL;

    /* Input buffer */
    ib = bufnew(1);
    bufputs(ib, input_text);

    /* Output buffer */
    ob = bufnew(1);

    /* Parse Markdown */
    ups_xhtml_renderer(&renderer, 0);
    ups_markdown(ob, ib, &renderer, 0xFF);
    ups_free_renderer(&renderer);

    bufnullterm(ob);
    output_text = strdup(ob->data);

    /* Cleanup */
    bufrelease(ib);
    bufrelease(ob);

    return Py_BuildValue("s", output_text);
}


static PyMethodDef PantyshotMethods[] = {
    {"render",  pantyshot_markdown, METH_VARARGS, pantyshot_render__doc__},
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