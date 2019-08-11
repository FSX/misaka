#include <string.h>

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

#define MEMBUF_PUT_LITERAL(out, literal) membuf_append((out), (literal), (MD_SIZE) strlen(literal))

// From md4c/render_html.c
#define ISDIGIT(ch)     ('0' <= (ch) && (ch) <= '9')
#define ISLOWER(ch)     ('a' <= (ch) && (ch) <= 'z')
#define ISUPPER(ch)     ('A' <= (ch) && (ch) <= 'Z')
#define ISALNUM(ch)     (ISLOWER(ch) || ISUPPER(ch) || ISDIGIT(ch))

// From md4c/render_html.c, modified to work stand-alone.
void misaka_escape_html(struct membuffer* out, const MD_CHAR* data, MD_SIZE size)
{
    static char escape_map[256] = {
        [(unsigned char)'"']=1,
        [(unsigned char)'&']=1,
        [(unsigned char)'<']=1,
        [(unsigned char)'>']=1,
    };

    MD_OFFSET beg = 0;
    MD_OFFSET off = 0;

    /* Some characters need to be escaped in normal HTML text. */
    #define HTML_NEED_ESCAPE(ch) (escape_map[(unsigned char)(ch)] != 0)

    while(1) {
        /* Optimization: Use some loop unrolling. */
        while(off + 3 < size  &&  !HTML_NEED_ESCAPE(data[off+0])  &&  !HTML_NEED_ESCAPE(data[off+1])
                              &&  !HTML_NEED_ESCAPE(data[off+2])  &&  !HTML_NEED_ESCAPE(data[off+3])) {
            off += 4;
        }

        while(off < size  &&  !HTML_NEED_ESCAPE(data[off])) {
            off++;
        }

        if(off > beg) {
            membuf_append(out, data + beg, off - beg);
        }

        if(off < size) {
            switch(data[off]) {
                case '&':   MEMBUF_PUT_LITERAL(out, "&amp;"); break;
                case '<':   MEMBUF_PUT_LITERAL(out, "&lt;"); break;
                case '>':   MEMBUF_PUT_LITERAL(out, "&gt;"); break;
                case '"':   MEMBUF_PUT_LITERAL(out, "&quot;"); break;
            }
            off++;
        } else {
            break;
        }

        beg = off;
    }
}

// From md4c/render_html.c, modified to work stand-alone.
void misaka_escape_url(struct membuffer* out, const MD_CHAR* data, MD_SIZE size)
{
    static const MD_CHAR hex_chars[] = "0123456789ABCDEF";
    MD_OFFSET beg = 0;
    MD_OFFSET off = 0;

    #define URL_NEED_ESCAPE(ch)                                             \
            (!ISALNUM(ch)  &&  strchr("-_.+!*'(),%#@?=;:/,+$", ch) == NULL)

    while(1) {
        while(off < size  &&  !URL_NEED_ESCAPE(data[off])) {
            off++;
        }

        if(off > beg) {
            membuf_append(out, data + beg, off - beg);
        }

        if(off < size) {
            char hex[3];

            switch(data[off]) {
                case '&':   MEMBUF_PUT_LITERAL(out, "&amp;"); break;
                case '\'':  MEMBUF_PUT_LITERAL(out, "&#x27;"); break;
                default:
                    hex[0] = '%';
                    hex[1] = hex_chars[((unsigned)data[off] >> 4) & 0xf];
                    hex[2] = hex_chars[((unsigned)data[off] >> 0) & 0xf];
                    membuf_append(out, hex, 3);
                    break;
            }
            off++;
        } else {
            break;
        }

        beg = off;
    }
}

// From md4c/render_html.c, modified to work stand-alone.
void misaka_codepoint_to_utf8(struct membuffer* out, unsigned codepoint)
{
    static const MD_CHAR utf8_replacement_char[] = { 0xef, 0xbf, 0xbd };

    unsigned char utf8[4];
    size_t n;

    if(codepoint <= 0x7f) {
        n = 1;
        utf8[0] = codepoint;
    } else if(codepoint <= 0x7ff) {
        n = 2;
        utf8[0] = 0xc0 | ((codepoint >>  6) & 0x1f);
        utf8[1] = 0x80 + ((codepoint >>  0) & 0x3f);
    } else if(codepoint <= 0xffff) {
        n = 3;
        utf8[0] = 0xe0 | ((codepoint >> 12) & 0xf);
        utf8[1] = 0x80 + ((codepoint >>  6) & 0x3f);
        utf8[2] = 0x80 + ((codepoint >>  0) & 0x3f);
    } else {
        n = 4;
        utf8[0] = 0xf0 | ((codepoint >> 18) & 0x7);
        utf8[1] = 0x80 + ((codepoint >> 12) & 0x3f);
        utf8[2] = 0x80 + ((codepoint >>  6) & 0x3f);
        utf8[3] = 0x80 + ((codepoint >>  0) & 0x3f);
    }

    if(0 < codepoint  &&  codepoint <= 0x10ffff) {
        membuf_append(out, (char*)utf8, n);
    } else {
        membuf_append(out, utf8_replacement_char, 3);
    }
}
