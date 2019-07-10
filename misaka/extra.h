#ifndef MISAKA_EXTRA_H
#define MISAKA_EXTRA_H

#ifdef __cplusplus
    extern "C" {
#endif

int misaka_render_html(
    const MD_CHAR* input, MD_SIZE input_size,
    void* userdata,
    unsigned parser_flags,
    unsigned renderer_flags
);

#ifdef __cplusplus
    }  /* extern "C" { */
#endif

#endif  /* MISAKA_EXTRA_H */
