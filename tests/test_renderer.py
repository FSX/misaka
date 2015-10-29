# -*- coding: utf-8 -*-

# These tests are mostly based on Hoep's custom renderer tests:
# https://github.com/Anomareh/Hoep/blob/master/test/custom_renderer.py

from textwrap import dedent

import misaka as m
from chibitest import TestCase, ok


tests = (
    ('blockcode', {
        'supplied': '```bash\n$ :(){ :|:& };:\n```',
        'expected': '[BLOCKCODE language=bash] $ :(){ :|:& };:\n'
    }),
    ('blockquote', {
        'supplied': '> This is a blockquote!',
        'expected': '[BLOCKQUOTE] [PARAGRAPH] This is a blockquote!\n\n'
    }),
    ('header', {
        'supplied': '## Level 2 header',
        'expected': '[HEADER level=2] Level 2 header'
    }),
    ('hrule', {
        'supplied': '---',
        'expected': '[HRULE]'
    }),
    ('ordered_list', {
        'supplied': """\
            1. One
            2. Two
            3. Three
            4. Four
            """,
        'expected': """\
            [LIST ordered=true block=false]
            [LISTITEM ordered=true block=false] One
            [LISTITEM ordered=true block=false] Two
            [LISTITEM ordered=true block=false] Three
            [LISTITEM ordered=true block=false] Four
            """
    }),
    ('unordered_list', {
        'supplied': """\
             - One
             - Two
             - Three
             - Four
            """,
        'expected': """\
            [LIST ordered=false block=false]
            [LISTITEM ordered=false block=false] One
            [LISTITEM ordered=false block=false] Two
            [LISTITEM ordered=false block=false] Three
            [LISTITEM ordered=false block=false] Four
            """
    }),
    ('unordered_list_block', {
        'supplied': """\
             - One

             - Two

             - Three

             - Four
             """,
        'expected': """\
            [LIST ordered=false block=true]
            [LISTITEM ordered=false block=true] [PARAGRAPH] One
            [LISTITEM ordered=false block=true] [PARAGRAPH] Two
            [LISTITEM ordered=false block=true] [PARAGRAPH] Three
            [LISTITEM ordered=false block=true] [PARAGRAPH] Four
            """
    }),
    ('table', {
        'supplied': """\
            |  1  |  2  |  3  |
            | --- |:---:| ---:|
            |  X  |  X  |  O  |
            |  O  |  O  |  X  |
            |  X  |  O  |  X  |
            """,
        'expected': """\
            [TABLE]
            [TABLE_HEADER]
            [TABLE_ROW]
            [TABLE_CELL header=true text=1][TABLE_CELL header=true align=center text=2][TABLE_CELL header=true align=right text=3]
            [TABLE_BODY]
            [TABLE_ROW]
            [TABLE_CELL text=X][TABLE_CELL align=center text=X][TABLE_CELL align=right text=O]
            [TABLE_ROW]
            [TABLE_CELL text=O][TABLE_CELL align=center text=O][TABLE_CELL align=right text=X]
            [TABLE_ROW]
            [TABLE_CELL text=X][TABLE_CELL align=center text=O][TABLE_CELL align=right text=X]
            """
    }),
    ('footnotes', {
        'supplied': 'What you looking at? [^1]\n\n[^1]: Yeah, I\'m talking to you pal.',
        'expected': """\
            [PARAGRAPH] What you looking at? [FOOTNOTE_REF number=1]
            [FOOTNOTES]
            [FOOTNOTE_DEF number=1] [PARAGRAPH] Yeah, I'm talking to you pal.
            """
    }),
    ('blockhtml', {
        'supplied': '<p>Hello!</p>',
        'expected': '[BLOCKHTML] <p>Hello!</p>\n'
    }),
    ('paragraph', {
        'supplied': 'This is a paragraph!',
        'expected': '[PARAGRAPH] This is a paragraph!\n'
    }),
    ('autolink', {
        'supplied': 'https://github.com/',
        'expected': '[PARAGRAPH] [AUTOLINK email=false] https://github.com/\n'
    }),
    ('codespan', {
        'supplied': '`some inline code`',
        'expected': '[PARAGRAPH] [CODESPAN] some inline code\n'
    }),
    ('double_emphasis', {
        'supplied': '__some double emphasis here__',
        'expected': '[PARAGRAPH] [DOUBLE_EMPHASIS] some double emphasis here\n'
    }),
    ('emphasis', {
        'supplied': '_some emphasis here_',
        'expected': '[PARAGRAPH] [EMPHASIS] some emphasis here\n'
    }),
    ('highlight', {
        'supplied': '==blink==',
        'expected': '[PARAGRAPH] [HIGHLIGHT] blink\n'
    }),
    ('quote', {
        'supplied': '"Inline quote here"',
        'expected': '[PARAGRAPH] [QUOTE] Inline quote here\n'
    }),
    ('image', {
        'supplied': '![spacer](spacer.gif "spacer")',
        'expected': '[PARAGRAPH] [IMAGE link=spacer.gif title=spacer alt=spacer]\n'
    }),
    ('image_ref', {
        'supplied': '![spacer][spacer]\n\n[spacer]: spacer.gif',
        'expected': '[PARAGRAPH] [IMAGE link=spacer.gif title= alt=spacer]\n'
    }),
    ('linebreak', {
        'supplied': 'Break  \nlines!',
        'expected': '[PARAGRAPH] Break[LINEBREAK]lines!\n'
    }),
    ('link', {
        'supplied': '[GitHub](https://github.com/)',
        'expected': '[PARAGRAPH] [LINK link=https://github.com/ title=] GitHub\n'
    }),
    ('link_ref', {
        'supplied': '[GitHub][github]\n\n[github]: https://github.com/ "GitHub"',
        'expected': '[PARAGRAPH] [LINK link=https://github.com/ title=GitHub] GitHub\n'
    }),
    ('triple_emphasis', {
        'supplied': '___too much emphasis here___',
        'expected': '[PARAGRAPH] [TRIPLE_EMPHASIS] too much emphasis here\n'
    }),
    ('strikethrough', {
        'supplied': '~~strike!~~',
        'expected': '[PARAGRAPH] [STRIKETHROUGH] strike!\n'
    }),
    ('superscript', {
        'supplied': '^super',
        'expected': '[PARAGRAPH] [SUPERSCRIPT] super\n'
    }),
    ('raw_html', {
        'supplied': '<bleep/>',
        'expected': '[PARAGRAPH] [RAW_HTML_TAG] <bleep/>\n'
    }),
    ('underline', {
        'render': 'underline',
        'supplied': 'some _underline_ here',
        'expected': '[PARAGRAPH] some [UNDERLINE] underline here\n'
    }),
    ('doc_header_and_footer', {
        'render': 'hf',
        'supplied': 'Text',
        'expected': '[DOC_HEADER]\n[PARAGRAPH] Text\n[DOC_FOOTER]\n'
    }),
    ('lowlevel', {
        'render': 'lowlevel',
        'supplied': '&#9731;',
        'expected': '[NORMAL_TEXT] [ENTITY] &#9731;'
    }),
    ('math_inline', {
        'supplied': 'Some math $$1*2*3 math with dollar$$',
        'expected': '[PARAGRAPH] Some math [MATH] 1*2*3 math with dollar\n'
    }),
)


class TestRenderer(m.BaseRenderer):
    def blockcode(self, text, language):
        return '[BLOCKCODE language={1}] {0}'.format(text, language)

    def blockquote(self, content):
        return '[BLOCKQUOTE] {0}\n'.format(content)

    def header(self, content, level):
        return '[HEADER level={1}] {0}'.format(content, level)

    def hrule(self):
        return '[HRULE]'

    def list(self, content, is_ordered, is_block):
        ordered = 'true' if is_ordered else 'false'
        block = 'true' if is_block else 'false'
        return '[LIST ordered={1} block={2}]\n{0}'.format(content, ordered, block)

    def listitem(self, content, is_ordered, is_block):
        ordered = 'true' if is_ordered else 'false'
        block = 'true' if is_block else 'false'
        return '[LISTITEM ordered={1} block={2}] {0}'.format(content, ordered, block)

    def paragraph(self, text):
        return '[PARAGRAPH] {0}\n'.format(text)

    def table(self, content):
        return '[TABLE]\n{0}'.format(content)

    def table_header(self, content):
        return '[TABLE_HEADER]\n{0}'.format(content)

    def table_body(self, content):
        return '[TABLE_BODY]\n{0}'.format(content)

    def table_row(self, content):
        return '[TABLE_ROW]\n{0}\n'.format(content)

    def table_cell(self, text, align, is_header):
        align = 'align={0} '.format(align) if align else ''
        header = 'header=true ' if is_header else ''
        return '[TABLE_CELL {2}{1}text={0}]'.format(text, align, header)

    def footnotes(self, text):
        return '[FOOTNOTES]\n{0}'.format(text)

    def footnote_def(self, text, number):
        return '[FOOTNOTE_DEF number={1}] {0}'.format(text, number)

    def footnote_ref(self, number):
        return '[FOOTNOTE_REF number={0}]'.format(number)

    def blockhtml(self, text):
        return '[BLOCKHTML] {0}'.format(text)

    def autolink(self, link, is_email):
        email = 'true' if is_email else 'false'
        return '[AUTOLINK email={1}] {0}'.format(link, email)

    def codespan(self, text):
        return '[CODESPAN] {0}'.format(text)

    def double_emphasis(self, text):
        return '[DOUBLE_EMPHASIS] {0}'.format(text)

    def emphasis(self, text):
        return '[EMPHASIS] {0}'.format(text)

    def underline(self, text):
        return '[UNDERLINE] {0}'.format(text)

    def highlight(self, text):
        return '[HIGHLIGHT] {0}'.format(text)

    def quote(self, text):
        return '[QUOTE] {0}'.format(text)

    def image(self, link, title, alt):
        return '[IMAGE link={0} title={1} alt={2}]'.format(link, title, alt)

    def linebreak(self):
        return '[LINEBREAK]'

    def link(self, content, link, title):
        return '[LINK link={0} title={1}] {2}'.format(link, title, content)

    def strikethrough(self, text):
        return '[STRIKETHROUGH] {0}'.format(text)

    def superscript(self, text):
        return '[SUPERSCRIPT] {0}'.format(text)

    def raw_html(self, text):
        return '[RAW_HTML_TAG] {0}'.format(text)

    def triple_emphasis(self, text):
        return '[TRIPLE_EMPHASIS] {0}'.format(text)

    def math(self, text, displaymode):
        return '[MATH] {0}'.format(text)

    def normal_text(self, text):
        return text


class TestRendererHeaderFooter(TestRenderer):
    def doc_header(self, inline_render):
        return '[DOC_HEADER]\n'

    def doc_footer(self, inline_render):
        return '[DOC_FOOTER]\n'


class TestRendererLowlevel(m.BaseRenderer):
    def paragraph(self, text):
        return text

    def entity(self, text):
        return '[ENTITY] {0}'.format(text)

    def normal_text(self, text):
        return '[NORMAL_TEXT] {0}'.format(text)


class CustomRendererTest(TestCase):
    def setup(self):
        render_default = m.Markdown(
            TestRenderer(), (
                'fenced-code',
                'tables',
                'footnotes',
                'autolink',
                'highlight',
                'quote',
                'strikethrough',
                'superscript',
                'math'))

        # EXT_UNDERLINE Clashes with emphasis.
        render_underline = m.Markdown(TestRenderer(), ('underline',))
        render_lowlevel = m.Markdown(TestRendererLowlevel())
        render_hf = m.Markdown(TestRendererHeaderFooter())

        self.md = {
            'default': render_default,
            'underline': render_underline,
            'lowlevel': render_lowlevel,
            'hf': render_hf,
        }

        for name, data in tests:
            self._create_test(name, data)

    def _create_test(self, name, data):
        render = self.md['default']
        supplied = data['supplied']
        expected = data['expected']

        if 'render' in data:
            render = self.md.get(data['render'])
        if not ('options' in data and 'no_dedent' in data['options']):
            supplied = dedent(data['supplied'])
            expected = dedent(data['expected'])

        def test():
            ok(render(supplied)).diff(expected)

        test.__name__ = 'test_' + name
        self.add_test(test)
