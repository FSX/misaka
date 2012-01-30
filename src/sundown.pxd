from libc.stdint cimport uint8_t


cdef extern from 'sundown/buffer.h':
    struct buf:
        uint8_t *data
        size_t size
        size_t asize
        size_t unit

    buf* bufnew(size_t)
    int bufgrow(buf *, size_t)
    void bufcstr(buf *)
    void bufrelease(buf *)
    void bufputs(buf *, char *)


cdef extern from 'sundown/html.h':
    struct _toc_data_st:
        int header_count
        int current_level

    struct html_renderopt:
        _toc_data_st toc_data
        unsigned int flags
        void (*link_attributes)(buf *ob, buf *url, void *self)

    void sdhtml_renderer(
        sd_callbacks *callbacks,
        html_renderopt *options_ptr,
        unsigned int render_flags)
    void sdhtml_toc_renderer(
        sd_callbacks *callbacks,
        html_renderopt *options_ptr)
    void sdhtml_smartypants(
        buf *ob,
        uint8_t *text,
        size_t size)


cdef extern from 'sundown/markdown.h':
    enum mkd_autolink:
        pass

    struct sd_callbacks:
        # Block level callbacks - NULL skips the block
        void (*blockcode)(buf *ob, buf *text, buf *lang, void *opaque)
        void (*blockquote)(buf *ob, buf *text, void *opaque)
        void (*blockhtml)(buf *ob, buf *text, void *opaque)
        void (*header)(buf *ob, buf *text, int level, void *opaque)
        void (*hrule)(buf *ob, void *opaque)
        void (*list)(buf *ob, buf *text, int flags, void *opaque)
        void (*listitem)(buf *ob, buf *text, int flags, void *opaque)
        void (*paragraph)(buf *ob, buf *text, void *opaque)
        void (*table)(buf *ob, buf *header, buf *body, void *opaque)
        void (*table_row)(buf *ob, buf *text, void *opaque)
        void (*table_cell)(buf *ob, buf *text, int flags, void *opaque)

        # Span level callbacks - NULL or return 0 prints the span verbatim
        int (*autolink)(buf *ob, buf *link, mkd_autolink type, void *opaque)
        int (*codespan)(buf *ob, buf *text, void *opaque)
        int (*double_emphasis)(buf *ob, buf *text, void *opaque)
        int (*emphasis)(buf *ob, buf *text, void *opaque)
        int (*image)(buf *ob, buf *link, buf *title, buf *alt, void *opaque)
        int (*linebreak)(buf *ob, void *opaque)
        int (*link)(buf *ob, buf *link, buf *title, buf *content, void *opaque)
        int (*raw_html_tag)(buf *ob, buf *tag, void *opaque)
        int (*triple_emphasis)(buf *ob, buf *text, void *opaque)
        int (*strikethrough)(buf *ob, buf *text, void *opaque)
        int (*superscript)(buf *ob, buf *text, void *opaque)

        # Low level callbacks - NULL copies input directly into the output
        void (*entity)(buf *ob, buf *entity, void *opaque)
        void (*normal_text)(buf *ob, buf *text, void *opaque)

        # Header and footer
        void (*doc_header)(buf *ob, void *opaque)
        void (*doc_footer)(buf *ob, void *opaque)

    enum mkd_autolink:
        pass

    struct sd_markdown:
        pass

    sd_markdown *sd_markdown_new(
        unsigned int extensions,
        size_t max_nesting,
        sd_callbacks *callbacks,
        html_renderopt *opaque)
    void sd_markdown_render(
        buf *ob,
        uint8_t *document,
        size_t doc_size,
        sd_markdown *md)
    void sd_markdown_free(sd_markdown *md)
    void sd_version(int *major, int *minor, int *revision)
