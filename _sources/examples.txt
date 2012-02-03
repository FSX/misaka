.. _examples:

Examples
========

Here are some example of custom renderers and pre- and postprocessors.


Extensions & flags
------------------

All extensions and flags are listed under constants on the :doc:`/api` page.
Both are pass as an argument to the renderer or the parser. For example::

    html('some ~~markdown~~ ^text',
        extensions=EXT_STRIKETHROUGH | EXT_SUPERSCRIPT,
        render_flags=HTML_SMARTYPANTS | HTML_USE_XHTML)

Or::

    rndr = HtmlRenderer(HTML_USE_XHTML | HTML_ESCAPE)
    md = Markdown(rndr, EXT_STRIKETHROUGH | EXT_SUPERSCRIPT)

    md.render('some ~~markdown~~ ^text')


Renderer callbacks
------------------

Here is a list of methods (with the arguments they accept) that can be
implemented in a renderer. None of these methods are already in the
:py:class:`BaseRenderer`. It just puts all the methods it recognizes in the
callback list.

**Block-level**::

    block_code(code, language)
    block_quote(quote)
    block_html(raw_html)
    header(text, level)
    hrule()
    list(contents, is_ordered)
    list_item(text, is_ordered)
    paragraph(text)
    table(header, body)
    table_row(content)
    table_cell(content, flags)

The ``flags`` argument contains the alignment of the cell and if it's an
header cell or not.


**Span-level**::

    autolink(link, is_email)
    codespan(code)
    double_emphasis(text)
    emphasis(text)
    image(link, title, alt_text)
    linebreak()
    link(link, title, content)
    raw_html(raw_html)
    triple_emphasis(text)
    strikethrough(text)
    superscript(text)

**Low-level**::

    entity(text)
    normal_text(text)

**Header and footer of the document**::

    doc_header()
    doc_footer()

**Pre- and post-process**::

    preprocess(full_document)
    postprocess(full_document)


A custom renderer
-----------------

It's actually pretty easy::

    from misaka import Markdown, BaseRenderer, HtmlRenderer, SmartyPants, \
        EXT_FENCED_CODE, EXT_TABLES, EXT_AUTOLINK, EXT_STRIKETHROUGH, \
        EXT_SUPERSCRIPT, HTML_USE_XHTML, \
        TABLE_ALIGN_L, TABLE_ALIGN_R, TABLE_ALIGN_C, \
        TABLE_ALIGNMASK, TABLE_HEADER


    class BleepRenderer(HtmlRenderer):

        def block_code(self, text, lang):
            if lang:
                lang = ' class="%s"' % lang
            else:
                lang  = ''
            return '\n<pre%s><code>%s</code></pre>\n' % (lang, text)

        def hrule(self):
            if self.flags & HTML_USE_XHTML:
                return '\n<hr/>\n'
            else:
                return '\n<hr>\n'

        def list(self, text, is_ordered):
            if is_ordered:
                return '\n<ol>%s</ol>\n' % text
            else:
                return '\n<ul>%s</ul>\n' % text

        def list_item(self, text, is_ordered):
            return '<li>%s</li>\n' % text

        def table(self, header, body):
            return '\n<table><thead>\n%s</thead><tbody>\n%s</tbody></table>\n' % \
                (header, body)

        def table_row(self, text):
            return '<tr>\n%s</tr>\n' % text

        def table_cell(self, text, flags):
            flags = flags & TABLE_ALIGNMASK
            if flags == TABLE_ALIGN_C:
                align = 'align="center"'
            elif flags == TABLE_ALIGN_L:
                align = 'align="left"'
            elif flags == TABLE_ALIGN_R:
                align = 'align="right"'
            else:
                align = ''

            if flags & TABLE_HEADER:
                return '<th%s>%s</th>\n' % (align, text)
            else:
                return '<td%s>%s</td>\n' % (align, text)

        def autolink(self, link, is_email):
            if is_email:
                return '<a href="mailto:%(link)s">%(link)s</a>' % {'link': link}
            else:
                return '<a href="%(link)s">%(link)s</a>' % {'link': link}


    md = Markdown(BleepRenderer(),
        EXT_FENCED_CODE | EXT_TABLES | EXT_AUTOLINK |
        EXT_STRIKETHROUGH | EXT_SUPERSCRIPT)


    print(md.render(u'''
    Unordered

    - One
    - Two
    - Three

    And now ordered:

    1. Three
    2. Two
    3. One

    An email: example@example.com

    And an URL: http://example.com
    '''))


Pre- or post-processor
----------------------

A pre- or post-processor is just a method called ``preprocess`` or ``postprocess``
that accepts one argument with the complete text. Or a class with one (or both)
of these methods. For example::

    class ExamplePreprocessor(object):
        def preprocess(self, text):
            return text.replace(' ', '_')

    class BleepRenderer(HtmlRenderer, ExamplePreprocessor):
        pass


Or::

    class BleepRenderer(HtmlRenderer):

        def preprocess(self, text):
            return text.replace(' ', '_')

Same rules apply for the post-processor, but you'll be processing text that's
already rendered.
