# -*- coding: utf-8 -*-

from chibitest import runner

from test_markdown import MarkdownConformanceTest_10, MarkdownConformanceTest_103
from test_renderer import CustomRendererTest


def run_tests():
    runner([
        # MarkdownConformanceTest_10,
        # MarkdownConformanceTest_103,
        CustomRendererTest,
    ])


if __name__ == '__main__':
    run_tests()
