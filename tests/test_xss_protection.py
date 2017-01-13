# -*- coding: utf-8 -*-

from chibitest import TestCase, ok
from misaka import escape_html, Markdown, SaferHtmlRenderer


class EscapeHtmlTest(TestCase):
    def test_escape_html(self):
        ok(escape_html('a&<>"\'/')) == 'a&amp;&lt;&gt;&quot;&#39;/'

    def test_escape_html_slash(self):
        ok(escape_html('a&<>"\'/', True)) == 'a&amp;&lt;&gt;&quot;&#39;&#47;'


render = Markdown(SaferHtmlRenderer())
render_escape = Markdown(SaferHtmlRenderer(sanitization_mode='escape'))


class SaferHtmlRendererTest(TestCase):
    def test_html_skip(self):
        actual = render('Example <script>alert(1);</script>')
        expected = '<p>Example alert(1);</p>\n'
        ok(actual).diff(expected)

        html = render('<sc<script>ript>xss</sc</script>ript>')
        ok(html).not_contains('<sc')
        ok(html).not_contains('ript>')

        actual = render('<span><a href="javascript:xss">foo</a></span>')
        expected = '<p>foo</p>\n'
        ok(actual).diff(expected)

    def test_html_escape(self):
        supplied = 'Example <script>alert(1);</script>'
        expected = '<p>%s</p>\n' % escape_html(supplied)
        ok(render_escape(supplied)).diff(expected)

        html = render_escape('<sc<script>ript>xss</sc</script>ript>')
        ok(html).not_contains('<sc')
        ok(html).not_contains('ript>')

        supplied = '<span><a href="javascript:xss">foo</a></span>'
        expected = '<p>%s</p>\n' % escape_html(supplied)
        ok(render_escape(supplied)).diff(expected)

    def test_autolink_filtering_with_nice_data(self):
        for url in ('http://a', "https://b?x&y"):
            actual = render('<%s>' % url)
            expected = '<p><a href="{0}">{0}</a></p>\n'.format(escape_html(url))
            ok(actual).diff(expected)

        supplied = "<alice@example.net>"
        expected = '<p>%s</p>\n' % escape_html(supplied)
        ok(render_escape(supplied)).diff(expected)

    def test_autolink_filtering_with_naughty_data(self):
        actual = render('<javascript:foo>')
        expected = '<p>&lt;javascript:foo&gt;</p>\n'
        ok(actual).diff(expected)

        link = 'javascript:0'
        encoded_link = ''.join('&x{0:x};'.format(ord(c)) for c in link)
        html = render('<%s>' % encoded_link)
        ok(html).not_contains(link)

    def test_link_filtering_with_nice_data(self):
        for url in ('http://a', 'https://b'):
            actual = render("['foo](%s \"bar'\")" % url)
            expected = '<p><a href="{0}" title="bar&#39;">&#39;foo</a></p>\n'.format(url)
            ok(actual).diff(expected)

    def test_link_filtering_with_naughty_data(self):
        supplied = '[foo](javascript:xss)'
        expected = '<p>%s</p>\n' % escape_html(supplied)
        ok(render(supplied)).diff(expected)

        html = render('[foo](unknown:bar)')
        expected = '<p>%s</p>\n' % escape_html(supplied)
        ok(render(supplied)).diff(expected)

        html = render('[" xss><xss>]("><xss>)')
        ok(html).not_contains('<xss>')
        ok(html).not_contains('" xss')
        html = render('[" xss><xss>](https:"><xss>)')
        ok(html).not_contains('<xss>')
        ok(html).not_contains('" xss')

    def test_image_src_filtering_with_nice_data(self):
        actual = render('![](http:"foo")')
        expected = '<p><img src="http:&quot;foo&quot;" /></p>\n'
        ok(actual).diff(expected)

        actual = render('!["bar"](https://example.org/ "\'title\'")')
        expected = '<p><img src="https://example.org/" alt="&quot;bar&quot;" title="&#39;title&#39;" /></p>\n'
        ok(actual).diff(expected)

    def test_image_src_filtering_with_naughty_data(self):
        actual = render('![foo](javascript:foo)')
        expected = '<p>![foo](javascript:foo)</p>\n'
        ok(actual).diff(expected)
