#include "hoedown/document.h"
#include "hoedown/html.h"

void *misaka_get_renderer(const hoedown_renderer_data *data) {
	// NOTE: Cast to a "hoedown_renderer_data *", because
	// the structure is assumed to have an "opaque" field.
	// Otherwise this doesn't work.
    return ((hoedown_renderer_data *) data->opaque)->opaque;
}
