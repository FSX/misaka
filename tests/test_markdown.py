# -*- coding: utf-8 -*-

import re
import codecs
from os import path
from glob import glob

from chibitest import TestCase, ok
from misaka import Markdown, HtmlRenderer
from utils import clean_html


class MarkdownConformanceTest_10(TestCase):
    """Markdown Conformance 1.0"""
    suite = 'MarkdownTest_1.0'

    def setup(self):
        self.r = Markdown(HtmlRenderer())

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
        return 'test_{0}'.format(name.lower())


class MarkdownConformanceTest_103(MarkdownConformanceTest_10):
    """Markdown Conformance 1.0.3"""
    suite = 'MarkdownTest_1.0.3'
