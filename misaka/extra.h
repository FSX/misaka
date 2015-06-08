/* extra.h - Helper functions */

#ifndef MICHIKO_EXTRA_H
#define MICHIKO_EXTRA_H

#include "hoedown/document.h"

#ifdef __cplusplus
extern "C" {
#endif

hoedown_renderer *null_renderer_new(void);
void null_renderer_free(hoedown_renderer *renderer);

#ifdef __cplusplus
}
#endif

#endif /** MICHIKO_EXTRA_H **/
