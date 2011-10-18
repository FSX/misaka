from sundown cimport buf, html_renderopt, mkd_autolink, sd_callbacks


cdef extern from *:
    ctypedef char* const_char_ptr "const char *"
    ctypedef char* const_size_t "const size_t"


cdef extern from 'wrapper.h':
    struct renderopt:
        html_renderopt html
        void *self

    sd_callbacks callback_funcs
    const_char_ptr method_names[]
    const_size_t method_count
