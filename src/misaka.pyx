cimport sundown
cimport wrapper

from libc.stdint cimport uint8_t


__version__ = '1.0.0'

# Markdown extensions
EXT_NO_INTRA_EMPHASIS = (1 << 0)
EXT_TABLES = (1 << 1)
EXT_FENCED_CODE = (1 << 2)
EXT_AUTOLINK = (1 << 3)
EXT_STRIKETHROUGH = (1 << 4)
EXT_LAX_HTML_BLOCKS = (1 << 5)
EXT_SPACE_HEADERS = (1 << 6)
EXT_SUPERSCRIPT = (1 << 7)

# HTML Render flags
HTML_SKIP_HTML = (1 << 0)
HTML_SKIP_STYLE = (1 << 1)
HTML_SKIP_IMAGES = (1 << 2)
HTML_SKIP_LINKS = (1 << 3)
HTML_EXPAND_TABS = (1 << 4)
HTML_SAFELINK = (1 << 5)
HTML_TOC = (1 << 6)
HTML_HARD_WRAP = (1 << 7)
HTML_USE_XHTML = (1 << 8)

# Extra HTML render flags - these are not from Sundown
HTML_SMARTYPANTS = (1 << 9)  # An extra flag to enable Smartypants
HTML_TOC_TREE = (1 << 10)  # Only render a table of contents tree


def html(object text, unsigned int extensions=0, unsigned int render_flags=0):

    # Convert string
    cdef bytes py_string = text.encode('UTF-8')
    cdef char *c_string = py_string
    del py_string

    # Definitions
    cdef sundown.sd_callbacks callbacks
    cdef sundown.html_renderopt options
    cdef sundown.sd_markdown *markdown

    # Buffers
    cdef sundown.buf *ib = sundown.bufnew(128)
    sundown.bufputs(ib, c_string)

    cdef sundown.buf *ob = sundown.bufnew(128)
    sundown.bufgrow(ob, <size_t> (ib.size * 1.4))

    # Renderer
    if render_flags & HTML_TOC_TREE:
        sundown.sdhtml_toc_renderer(&callbacks, &options)
    else:
        sundown.sdhtml_renderer(&callbacks, &options, render_flags)

    # Parser
    markdown = sundown.sd_markdown_new(extensions, 16, &callbacks, &options)
    sundown.sd_markdown_render(ob, ib.data, ib.size, markdown)
    sundown.sd_markdown_free(markdown)

    # Smartypantsu
    if render_flags & HTML_SMARTYPANTS:
        sb = sundown.bufnew(128)
        sundown.sdhtml_smartypants(sb, ob.data, ob.size)
        sundown.bufrelease(ob)
        ob = sb

    # Return a string and release buffers
    try:
        return (<char *> ob.data)[:ob.size].decode('UTF-8', 'strict')
    finally:
        sundown.bufrelease(ob)
        sundown.bufrelease(ib)


cdef class SmartyPants:
    def postprocess(self, object text):
        cdef bytes py_string = text.encode('UTF-8')
        cdef char *c_string = py_string
        del py_string

        cdef sundown.buf *ob = sundown.bufnew(128)
        sundown.sdhtml_smartypants(ob,
            <uint8_t *> c_string, len(text))

        try:
            return (<char *> ob.data)[:ob.size].decode('UTF-8', 'strict')
        finally:
            sundown.bufrelease(ob)


cdef class BaseRenderer:

    cdef sundown.sd_callbacks callbacks
    cdef wrapper.renderopt options
    cdef readonly int flags

    def __cinit__(self, int flags=0):
        self.options.self = <void *> self
        self.flags = flags
        self.setup()

        # Set callbacks
        cdef void **source = <void **> &wrapper.callback_funcs
        cdef void **dest = <void **> &self.callbacks

        for i from 0 <= i < <int> wrapper.method_count by 1:
            if hasattr(self, wrapper.method_names[i]):
                dest[i] = source[i]

    def setup(self):
        pass


cdef class HtmlRenderer(BaseRenderer):
    def setup(self):
        self.options.html.flags = self.flags
        sundown.sdhtml_renderer(
            &self.callbacks,
            &self.options.html,
            self.options.html.flags)


cdef class HtmlTocRenderer(BaseRenderer):
    def setup(self, int flags=0):
        sundown.sdhtml_toc_renderer(
            &self.callbacks,
            &self.options.html)


cdef class Markdown:

    cdef sundown.sd_markdown *markdown
    cdef BaseRenderer renderer

    def __cinit__(self, object renderer, int extensions=0):
        if not isinstance(renderer, BaseRenderer):
            raise ValueError('expected instance of BaseRenderer, %s found' % \
                renderer.__class__.__name__)

        self.renderer = <BaseRenderer> renderer
        self.markdown = sundown.sd_markdown_new(
            extensions, 16,
            &self.renderer.callbacks,
            <sundown.html_renderopt *> &self.renderer.options)

    def render(self, object text):
        if hasattr(self.renderer, 'preprocess'):
            text = self.renderer.preprocess(text)

        # Convert string
        cdef bytes py_string = text.encode('UTF-8')
        cdef char *c_string = py_string
        del py_string

        # Buffers
        cdef sundown.buf *ib = sundown.bufnew(128)
        sundown.bufputs(ib, c_string)

        cdef sundown.buf *ob = sundown.bufnew(128)
        sundown.bufgrow(ob, <size_t> (ib.size * 1.4))

        # Parse! And make a unicode string
        sundown.sd_markdown_render(ob, ib.data, ib.size, self.markdown)
        text = (<char *> ob.data)[:ob.size].decode('UTF-8', 'strict')

        if hasattr(self.renderer, 'postprocess'):
            text = self.renderer.postprocess(text)

        # Return a string and release buffers
        try:
            return text
        finally:
            sundown.bufrelease(ob)
            sundown.bufrelease(ib)

    def __dealloc__(self):
        if self.markdown is not NULL:
            sundown.sd_markdown_free(self.markdown)
