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
renderer_rewrite = SaferHtmlRenderer(
    link_rewrite='//example.com/redirect/{url}',
    img_src_rewrite='//img_proxy/{url}',
)
render_rewrite = Markdown(renderer_rewrite)
rewrite_url = renderer_rewrite.rewrite_url


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

        url = 'javascript:0'
        encoded_url = ''.join('&x{0:x};'.format(ord(c)) for c in url)
        html = render('<%s>' % encoded_url)
        ok(html).not_contains(url)

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

    def test_autolink_rewriting(self):
        for url in ('http://a', 'https://b?x&y'):
            actual = render_rewrite('<%s>' % url)
            expected = '<p><a href="%s">%s</a></p>\n'
            expected %= (rewrite_url(url), escape_html(url))
            ok(actual).diff(expected)

        supplied = "<alice@example.net>"
        expected = '<p>%s</p>\n' % escape_html(supplied)
        ok(render_escape(supplied)).diff(expected)

    def test_link_rewriting(self):
        for url in ('http://a', 'https://b'):
            actual = render_rewrite("['foo](%s \"bar'\")" % url)
            expected = '<p><a href="%s" title="bar&#39;">&#39;foo</a></p>\n' % rewrite_url(url)
            ok(actual).diff(expected)

    def test_image_src_rewriting(self):
        actual = render_rewrite('![](http:"foo")')
        expected = '<p><img src="//img_proxy/http%3A%22foo%22" /></p>\n'
        ok(actual).diff(expected)
