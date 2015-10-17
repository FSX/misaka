# -*- coding: utf-8 -*-

import sys
import time
from os.path import dirname, join as join_path

from chibitest import TestCase, Benchmark, ok


class BenchmarkLibraries(Benchmark):
    def setup(self):
        fp = join_path(dirname(__file__), 'data', 'markdown-syntax.md')
        with open(fp, 'r') as f:
            self.text = f.read()

        if sys.version_info[0] == 2:
            self.hoep_text = unicode(self.text)
        else:
            self.hoep_text = self.text

    def test_misaka(self):
        import misaka
        extensions = (
            'no-intra-emphasis',
            'fenced=code',
            'autolink',
            'tables',
            'strikethrough',
        )
        misaka.html(self.text, extensions)

    def test_misaka_classes(self):
        import misaka
        extensions = (
            'no-intra-emphasis',
            'fenced=code',
            'autolink',
            'tables',
            'strikethrough',
        )
        r = misaka.HtmlRenderer()
        p = misaka.Markdown(r, extensions)
        p(self.text)

    def test_mistune(self):
        import mistune
        mistune.markdown(self.text)

    def test_markdown(self):
        import markdown
        markdown.markdown(self.text, ['extra'])

    def test_markdown2(self):
        import markdown2
        extras = ['code-friendly', 'fenced-code-blocks', 'footnotes']
        markdown2.markdown(self.text, extras=extras)

    def test_hoep(self):
        import hoep as m
        extensions = (
            m.EXT_NO_INTRA_EMPHASIS | m.EXT_FENCED_CODE | m.EXT_AUTOLINK |
            m.EXT_TABLES | m.EXT_STRIKETHROUGH | m.EXT_FOOTNOTES)
        md = m.Hoep(extensions=extensions)
        md.render(self.hoep_text)
