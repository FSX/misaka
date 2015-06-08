#include "extra.h"

#include <string.h>

#include "hoedown/buffer.h"
#include "hoedown/document.h"


hoedown_renderer *null_renderer_new()
{
    hoedown_renderer *renderer;
    renderer = hoedown_malloc(sizeof(hoedown_renderer));
    memset(renderer, 0x0, sizeof(hoedown_renderer));

    return renderer;
}

void null_renderer_free(hoedown_renderer *renderer)
{
    free(renderer);
}
