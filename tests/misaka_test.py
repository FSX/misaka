# -*- coding: utf-8 -*-

import re
import unittest
from os import path
from glob import glob
from difflib import unified_diff

import misaka
from misaka import Markdown, BaseRenderer, HtmlRenderer, \
    SmartyPants, \
    HTML_ESCAPE

# from bs4 import BeautifulSoup


# class MarkdownTestCase(unittest.TestCase):

#     m = None

#     @classmethod
#     def generate_tests(cls):
#         tests_dir = path.dirname(__file__)
#         for fn in glob(path.join(tests_dir, 'MarkdownTest_1.0', '*.text')):
#             text, html = cls._get_data(fn)
#             setattr(cls, cls._generate_test_name(fn), cls._generate_test(text, html))

#     @classmethod
#     def _generate_test(cls, text, html):
#         def test(self):
#             self.assertMarkdown(text, html)
#         return test

#     @classmethod
#     def _generate_test_name(cls, text_path):
#         name = path.splitext(path.basename(text_path))[0]
#         name = name.replace(' - ', '_')
#         name = name.replace(' ', '_')
#         name = re.sub('[(),]', '', name)
#         return 'test_%s' % name.lower()

#     @classmethod
#     def _get_data(cls, text_path):
#         html_path = '%s.html' % path.splitext(text_path)[0]

#         with open(text_path, 'r') as fd:
#             text = fd.read()
#         with open(html_path, 'r') as fd:
#             html = fd.read()

#         return (text, html)

#     def setUp(self):
#         self.m = misaka

#     def assertMarkdown(self, text, html):

#         html = str(BeautifulSoup(html))
#         rndr_html = str(BeautifulSoup(self.m.html(text)))

#         if rndr_html != html:
#             udiff = unified_diff(
#                 html.splitlines(True),
#                 rndr_html.splitlines(True))
#             msg = self._formatMessage(None,
#                 'Rendered output not match expected output:\n%s' % ''.join(udiff))
#             raise self.fail(msg)


class SmartyPantsTest(unittest.TestCase):
    def setUp(self):
        self.pants = SmartyPants()

    def test_single_quotes_re(self):
        html = self.pants.postprocess('<p>They\'re not for sale.</p>')
        self.assertEqual('<p>They&rsquo;re not for sale.</p>', html)

    def test_single_quotes_ll(self):
        html = self.pants.postprocess('<p>Well that\'ll be the day</p>')
        self.assertEqual('<p>Well that&rsquo;ll be the day</p>', html)

    def test_double_quotes_to_curly_quotes(self):
        html = self.pants.postprocess('<p>"Quoted text"</p>')
        self.assertEqual('<p>&ldquo;Quoted text&rdquo;</p>', html)

    def test_single_quotes_ve(self):
        html = self.pants.postprocess('<p>I\'ve been meaning to tell you ..</p>')
        self.assertEqual('<p>I&rsquo;ve been meaning to tell you ..</p>', html)

    def test_single_quotes_m(self):
        html = self.pants.postprocess('<p>I\'m not kidding</p>')
        self.assertEqual('<p>I&rsquo;m not kidding</p>', html)

    def test_single_quotes_d(self):
        html = self.pants.postprocess('<p>what\'d you say?</p>')
        self.assertEqual('<p>what&rsquo;d you say?</p>', html)


if __name__ == '__main__':
    # MarkdownTestCase.generate_tests()
    unittest.main()
