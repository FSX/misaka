# -*- coding: utf-8 -*-

from misaka import Markdown, BaseRenderer, HtmlRenderer, \
    SmartyPants, \
    EXT_FENCED_CODE, EXT_TABLES, EXT_AUTOLINK, EXT_STRIKETHROUGH, \
    EXT_SUPERSCRIPT, HTML_USE_XHTML, \
    TABLE_ALIGN_L, TABLE_ALIGN_R, TABLE_ALIGN_C, \
    TABLE_ALIGNMASK, TABLE_HEADER


class BleepRenderer(HtmlRenderer, SmartyPants):

    def block_code(self, text, lang):
        if lang:
            lang = ' class="%s"' % lang
        else:
            lang  = ''
        return '\n<pre%s><code>%s</code></pre>\n' % (lang, text)

    def block_quote(self, text):
        return '\n<blockquote>%s</blockquote>\n' % text

    def block_html(self, text):
        return '\n%s' % text

    def header(self, text, level):
        return '\n<h%d>%s</h%d>\n' % (level, text, level)

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

    def paragraph(self, text):
        # No hard wrapping yet. Maybe with:
        # http://docs.python.org/library/textwrap.html
        return '\n<p>%s</p>\n' % text

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

    def preprocess(self, text):
        return text.replace(' ', '_')


md = Markdown(BleepRenderer(),
    EXT_FENCED_CODE | EXT_TABLES | EXT_AUTOLINK |
    EXT_STRIKETHROUGH | EXT_SUPERSCRIPT)


print(md.render('''
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
