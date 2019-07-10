#include "md4c/md4c.h"
#include "md4c/render_html.h"
#include "md4c/buffer.h"
#include "extra.h"

void process_output(const MD_CHAR* text, MD_SIZE size, void* userdata)
{
    membuf_append((struct membuffer*) userdata, text, size);
}

int misaka_render_html(
    const MD_CHAR* input, MD_SIZE input_size,
    void* userdata,
    unsigned parser_flags,
    unsigned renderer_flags
) {
    return md_render_html(input, input_size, process_output, userdata, parser_flags, renderer_flags);
}
