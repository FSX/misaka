# -*- coding: utf-8 -*-

# Most unit tests are based on the tests from Redcarpet.

import re
import codecs
from os import path
from glob import glob
from subprocess import Popen, PIPE, STDOUT

import misaka

from misaka import Markdown, BaseRenderer, HtmlRenderer, SmartyPants, \
    EXT_NO_INTRA_EMPHASIS, EXT_TABLES, EXT_FENCED_CODE, EXT_AUTOLINK, \
    EXT_STRIKETHROUGH, EXT_LAX_SPACING, EXT_SPACE_HEADERS, \
    EXT_SUPERSCRIPT, \
    HTML_SKIP_HTML, HTML_SKIP_STYLE, HTML_SKIP_IMAGES, HTML_SKIP_LINKS, \
    HTML_EXPAND_TABS, HTML_SAFELINK, HTML_TOC, HTML_HARD_WRAP, \
    HTML_USE_XHTML, HTML_ESCAPE, \
    HTML_SMARTYPANTS

from minitest import TestCase, ok, runner


def clean_html(dirty_html):
    input_html = dirty_html.encode('utf-8')
    p = Popen(['tidy', '--show-body-only', '1', '--quiet', '1', '--show-warnings', '0', '-utf8'],
        stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout, stderr = p.communicate(input=input_html)

    return stdout.decode('utf-8')


class SmartyPantsTest(TestCase):
    name = 'SmartyPants'

    def setup(self):
        self.r = lambda html: misaka.html(html, render_flags=HTML_SMARTYPANTS)

    def test_single_quotes_re(self):
        html = self.r('<p>They\'re not for sale.</p>\n')
        ok(html).diff('<p>They&rsquo;re not for sale.</p>\n')

    def test_single_quotes_ll(self):
        html = self.r('<p>Well that\'ll be the day</p>\n')
        ok(html).diff('<p>Well that&rsquo;ll be the day</p>\n')

    def test_double_quotes_to_curly_quotes(self):
        html = self.r('<p>"Quoted text"</p>\n')
        ok(html).diff('<p>&ldquo;Quoted text&rdquo;</p>\n')

    def test_single_quotes_ve(self):
        html = self.r('<p>I\'ve been meaning to tell you ..</p>\n')
        ok(html).diff('<p>I&rsquo;ve been meaning to tell you ..</p>\n')

    def test_single_quotes_m(self):
        html = self.r('<p>I\'m not kidding</p>\n')
        ok(html).diff('<p>I&rsquo;m not kidding</p>\n')

    def test_single_quotes_d(self):
        html = self.r('<p>what\'d you say?</p>\n')
        ok(html).diff('<p>what&rsquo;d you say?</p>\n')


class HtmlRenderTest(TestCase):
    name = 'Html Renderer'

    def setup(self):
        pants = SmartyPants()

        self.r = {
            HTML_SKIP_HTML: HtmlRenderer(HTML_SKIP_HTML),
            HTML_SKIP_IMAGES: HtmlRenderer(HTML_SKIP_IMAGES),
            HTML_SKIP_LINKS: HtmlRenderer(HTML_SKIP_LINKS),
            HTML_SAFELINK: HtmlRenderer(HTML_SAFELINK),
            HTML_ESCAPE: HtmlRenderer(HTML_ESCAPE),
            HTML_HARD_WRAP: HtmlRenderer(HTML_HARD_WRAP)
        }

    def render_with(self, flag, text):
        return Markdown(self.r[flag]).render(text)

    # Hint: overrides HTML_SKIP_HTML, HTML_SKIP_IMAGES and HTML_SKIP_LINKS
    def test_escape_html(self):
        source = '''
Through <em>NO</em> <script>DOUBLE NO</script>

<script>BAD</script>

<img src="/favicon.ico" />
'''

        expected = clean_html('''
<p>Through &lt;em&gt;NO&lt;/em&gt; &lt;script&gt;DOUBLE NO&lt;/script&gt;</p>

<p>&lt;script&gt;BAD&lt;/script&gt;</p>

<p>&lt;img src=&quot;/favicon.ico&quot; /&gt;</p>
''')

        markdown = clean_html(self.render_with(HTML_ESCAPE, source))
        ok(markdown).diff(expected)

    def test_skip_html(self):
        markdown = self.render_with(HTML_SKIP_HTML, 'Through <em>NO</em> <script>DOUBLE NO</script>')
        ok(markdown).diff('<p>Through NO DOUBLE NO</p>\n')

    def test_skip_html_two_space_hard_break(self):
        markdown = self.render_with(HTML_SKIP_HTML, 'Lorem,  \nipsum\n')
        ok(markdown).diff('<p>Lorem,<br>\nipsum</p>\n')

    def test_skip_image(self):
        markdown = self.render_with(HTML_SKIP_IMAGES, '![dust mite](http://dust.mite/image.png) <img src="image.png" />')
        ok(markdown).not_contains('<img')

    def test_skip_links(self):
        markdown = self.render_with(HTML_SKIP_LINKS, '[This link](http://example.net/) <a href="links.html">links</a>')
        ok(markdown).not_contains('<a ')

    def test_safelink(self):
        markdown = self.render_with(HTML_SAFELINK, '[IRC](irc://chat.freenode.org/#freenode)')
        ok(markdown).diff('<p>[IRC](irc://chat.freenode.org/#freenode)</p>\n')

    def test_hard_wrap(self):
        markdown = self.render_with(HTML_HARD_WRAP, '''
Hello world,
this is just a simple test

With hard wraps
and other *things*.''')
        ok(markdown).contains('<br>')


class MarkdownParserTest(TestCase):
    name = 'Markdown Parser'

    def setup(self):
        self.r = Markdown(HtmlRenderer()).render

    def render_with(self, text, flags=0, extensions=0):
        return Markdown(HtmlRenderer(), extensions).render(text)

    def test_one_liner_to_html(self):
        markdown = self.r('Hello World.')
        ok(markdown).diff('<p>Hello World.</p>\n')

    def test_inline_markdown_to_html(self):
        markdown = self.r('_Hello World_!')
        ok(markdown).diff('<p><em>Hello World</em>!</p>\n')

    def test_inline_markdown_start_end(self):
        markdown = self.render_with('_start _ foo_bar bar_baz _ end_ *italic* **bold** <a>_blah_</a>',
            extensions=EXT_NO_INTRA_EMPHASIS)
        ok(markdown).diff('<p><em>start _ foo_bar bar_baz _ end</em> <em>italic</em> <strong>bold</strong> <a><em>blah</em></a></p>\n')

        markdown = self.r('Run \'rake radiant:extensions:rbac_base:migrate\'')
        ok(markdown).diff('<p>Run &#39;rake radiant:extensions:rbac_base:migrate&#39;</p>\n')

    def test_urls_not_doubly_escaped(self):
        markdown = self.r('[Page 2](/search?query=Markdown+Test&page=2)')
        ok(markdown).diff('<p><a href="/search?query=Markdown+Test&amp;page=2">Page 2</a></p>\n')

    def test_inline_html(self):
        markdown = self.r('before\n\n<div>\n  foo\n</div>\n\nafter')
        ok(markdown).diff('<p>before</p>\n\n<div>\n  foo\n</div>\n\n<p>after</p>\n')

    def test_html_block_end_tag_on_same_line(self):
        markdown = self.r('Para 1\n\n<div><pre>HTML block\n</pre></div>\n\nPara 2 [Link](#anchor)')
        ok(markdown).diff('<p>Para 1</p>\n\n<div><pre>HTML block\n</pre></div>\n\n<p>Para 2 <a href=\"#anchor\">Link</a></p>\n')

    # This isn't in the spec but is Markdown.pl behavior.
    def test_block_quotes_preceded_by_spaces(self):
        markdown = self.r(
            'A wise man once said:\n\n' \
            ' > Isn\'t it wonderful just to be alive.\n')
        ok(markdown).diff(
            '<p>A wise man once said:</p>\n\n' \
            '<blockquote>\n<p>Isn&#39;t it wonderful just to be alive.</p>\n</blockquote>\n')

    def test_html_block_not_wrapped_in_p(self):
        markdown = self.render_with(
            'Things to watch out for\n\n' \
            '<ul>\n<li>Blah</li>\n</ul>\n',
            extensions=EXT_LAX_SPACING)
        ok(markdown).diff(
            '<p>Things to watch out for</p>\n\n' \
            '<ul>\n<li>Blah</li>\n</ul>\n')

    # http://github.com/rtomayko/rdiscount/issues/#issue/13
    def test_headings_with_trailing_space(self):
        markdown = self.render_with(
            'The Ant-Sugar Tales \n' \
            '=================== \n\n' \
            'By Candice Yellowflower   \n')
        ok(markdown).diff('<h1>The Ant-Sugar Tales </h1>\n\n<p>By Candice Yellowflower   </p>\n')

    def test_intra_emphasis(self):
        markdown = self.r('foo_bar_baz')
        ok(markdown).diff('<p>foo<em>bar</em>baz</p>\n')

        markdown = self.render_with('foo_bar_baz', extensions=EXT_NO_INTRA_EMPHASIS)
        ok(markdown).diff('<p>foo_bar_baz</p>\n')

    def test_autolink(self):
        markdown = self.render_with('http://axr.vg/', extensions=EXT_AUTOLINK)
        ok(markdown).diff('<p><a href=\"http://axr.vg/\">http://axr.vg/</a></p>\n')

    def test_tags_with_dashes_and_underscored(self):
        markdown = self.r('foo <asdf-qwerty>bar</asdf-qwerty> and <a_b>baz</a_b>')
        ok(markdown).diff('<p>foo <asdf-qwerty>bar</asdf-qwerty> and <a_b>baz</a_b></p>\n')

    def test_no_link_in_code_blocks(self):
        markdown = self.r('    This is a code block\n    This is a link [[1]] inside\n')
        ok(markdown).diff('<pre><code>This is a code block\nThis is a link [[1]] inside\n</code></pre>\n')

    def test_whitespace_after_urls(self):
        markdown = self.render_with('Japan: http://www.abc.net.au/news/events/japan-quake-2011/beforeafter.htm (yes, japan)',
            extensions=EXT_AUTOLINK)
        ok(markdown).diff('<p>Japan: <a href="http://www.abc.net.au/news/events/japan-quake-2011/beforeafter.htm">http://www.abc.net.au/news/events/japan-quake-2011/beforeafter.htm</a> (yes, japan)</p>\n')

    def test_infinite_loop_in_header(self):
        markdown = self.render_with(
            '######\n' \
            '#Body#\n' \
            '######\n')
        ok(markdown).diff('<h1>Body</h1>\n')

    def test_tables(self):
        text = ' aaa | bbbb\n' \
            '-----|------\n' \
            'hello|sailor\n'

        ok(self.render_with(text)).not_contains('<table')
        ok(self.render_with(text, extensions=EXT_TABLES)).contains('<table')

    def test_strikethrough(self):
        text = 'this is ~some~ striked ~~text~~'

        ok(self.render_with(text)).not_contains('<del')
        ok(self.render_with(text, extensions=EXT_STRIKETHROUGH)).contains('<del')

    def test_fenced_code_blocks(self):
        text = '''
This is a simple test

~~~~~
This is some awesome code
    with tabs and shit
~~~
'''

        ok(self.render_with(text)).not_contains('<code')
        ok(self.render_with(text, extensions=EXT_FENCED_CODE)).contains('<code')

    def test_fenced_code_blocks_without_space(self):
        text = 'foo\nbar\n```\nsome\ncode\n```\nbaz'

        ok(self.render_with(text)).not_contains('<pre><code>')
        ok(self.render_with(text, extensions=EXT_FENCED_CODE | EXT_LAX_SPACING)).contains('<pre><code>')

    def test_linkable_headers(self):
        markdown = self.r('### Hello [GitHub](http://github.com)')
        ok(markdown).diff('<h3>Hello <a href=\"http://github.com\">GitHub</a></h3>\n')

    def test_autolinking_with_ent_chars(self):
        markdown = self.render_with('This a stupid link: https://github.com/rtomayko/tilt/issues?milestone=1&state=open',
            extensions=EXT_AUTOLINK)
        ok(markdown).diff('<p>This a stupid link: <a href=\"https://github.com/rtomayko/tilt/issues?milestone=1&amp;state=open\">https://github.com/rtomayko/tilt/issues?milestone=1&amp;state=open</a></p>\n')

    def test_spaced_headers(self):
        text = '#123 a header yes\n'
        ok(self.render_with(text, extensions=EXT_SPACE_HEADERS)).not_contains('<h1>')


class MarkdownConformanceTest_10(TestCase):
    name = 'Markdown Conformance 1.0'
    suite = 'MarkdownTest_1.0'

    def setup(self):
        self.r = Markdown(HtmlRenderer()).render

        tests_dir = path.dirname(__file__)
        for text_path in glob(path.join(tests_dir, self.suite, '*.text')):
            html_path = '%s.html' % path.splitext(text_path)[0]
            self._create_test(text_path, html_path)

    def _create_test(self, text_path, html_path):
        def test():
            with codecs.open(text_path, 'r', encoding='utf-8') as fd:
                text = fd.read()
            with codecs.open(html_path, 'r', encoding='utf-8') as fd:
                expected_html = fd.read()

            actual_html = self.r(text)
            expected_result = clean_html(expected_html)
            actual_result = clean_html(actual_html)

            ok(actual_result).diff(expected_result)

        test.__name__ = self._test_name(text_path)
        self.add_test(test)

    def _test_name(self, text_path):
        name = path.splitext(path.basename(text_path))[0]
        name = name.replace(' - ', '_')
        name = name.replace(' ', '_')
        name = re.sub('[(),]', '', name)
        return 'test_%s' % name.lower()


class MarkdownConformanceTest_103(MarkdownConformanceTest_10):
    name = 'Markdown Conformance 1.0.3'
    suite = 'MarkdownTest_1.0.3'


class UnicodeTest(TestCase):
    name = 'Unicode'

    def setup(self):
        self.r = Markdown(HtmlRenderer()).render

    def test_unicode(self):
        tests_dir = path.dirname(__file__)

        with codecs.open(path.join(tests_dir, 'unicode.txt'), 'r', encoding='utf-8') as fd:
            text = fd.read()
        with codecs.open(path.join(tests_dir, 'unicode.html'), 'r', encoding='utf-8') as fd:
            html = fd.read()

        markdown = self.r(text)
        ok(markdown).diff(html)


if __name__ == '__main__':
    runner([
        SmartyPantsTest,
        HtmlRenderTest,
        MarkdownParserTest,
        MarkdownConformanceTest_10,
        MarkdownConformanceTest_103,
        UnicodeTest
    ])
