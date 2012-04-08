# -*- coding: utf-8 -*-

import re
from os import path
from glob import glob
from subprocess import Popen, PIPE, STDOUT

import misaka

from misaka import Markdown, BaseRenderer, HtmlRenderer, \
    SmartyPants, \
    HTML_ESCAPE, HTML_SMARTYPANTS, HTML_SKIP_HTML, HTML_SKIP_IMAGES, \
    HTML_SKIP_LINKS, HTML_ESCAPE, HTML_SAFELINK, HTML_HARD_WRAP
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
    name = 'SmartyPants'

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
            with open(text_path, 'r') as fd:
                text = fd.read()
            with open(html_path, 'r') as fd:
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


if __name__ == '__main__':
    runner([
        SmartyPantsTest,
        HtmlRenderTest,
        MarkdownConformanceTest_10,
        MarkdownConformanceTest_103
    ])
