#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sundown/html.h"


struct renderopt {
    struct html_renderopt html;
    void *self;
};


extern struct sd_callbacks callback_funcs;
extern const char *method_names[];
extern const size_t method_count;
