# -*- coding: utf-8 -*-

from chibitest import TestCase, ok
from misaka import smartypants


class SmartypantsTest(TestCase):
    def test_apostrophes(self):
        ok(smartypants('\'s')) == '&rsquo;s'
        ok(smartypants('\'t')) == '&rsquo;t'
        ok(smartypants('\'m')) == '&rsquo;m'
        ok(smartypants('\'d')) == '&rsquo;d'
        ok(smartypants('\'re')) == '&rsquo;re'
        ok(smartypants('\'ll')) == '&rsquo;ll'
        ok(smartypants('\'ve')) == '&rsquo;ve'

    def test_double_quotes(self):
        ok(smartypants('"Quotes"')) == '&ldquo;Quotes&rdquo;'

    def test_dash(self):
        ok(smartypants('--')) == '&ndash;'
        ok(smartypants('---')) == '&mdash;'

    def test_ellipsis(self):
        ok(smartypants('...')) == '&hellip;'
        ok(smartypants('. . .')) == '&hellip;'

    def test_parens(self):
        ok(smartypants('(c)')) == '&copy;'
        ok(smartypants('(r)')) == '&reg;'
        ok(smartypants('(tm)')) == '&trade;'

    def test_fractions(self):
        ok(smartypants('3/4ths')) == '&frac34;ths'
        ok(smartypants('3/4')) == '&frac34;'
        ok(smartypants('1/2')) == '&frac12;'
        ok(smartypants('1/4')) == '&frac14;'
