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

void misaka_escape_html(struct membuffer* out, const MD_CHAR* data, MD_SIZE size);
void misaka_escape_url(struct membuffer* out, const MD_CHAR* data, MD_SIZE size);
void misaka_codepoint_to_utf8(struct membuffer* out, unsigned codepoint);

#ifdef __cplusplus
    }  /* extern "C" { */
#endif

#endif  /* MISAKA_EXTRA_H */
