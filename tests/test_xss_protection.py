# -*- coding: utf-8 -*-

from chibitest import TestCase, ok
from misaka import escape_html


class EscapeHtmlTest(TestCase):
    def test_escape_html(self):
        ok(escape_html('a&<>"\'/')) == 'a&amp;&lt;&gt;&quot;&#39;/'

    def test_escape_html_slash(self):
        ok(escape_html('a&<>"\'/', True)) == 'a&amp;&lt;&gt;&quot;&#39;&#47;'
