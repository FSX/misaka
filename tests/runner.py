# -*- coding: utf-8 -*-

import sys
import inspect

from chibitest import runner, TestCase

from test_markdown import MarkdownConformanceTest_10, MarkdownConformanceTest_103
from test_renderer import CustomRendererTest
from test_smartypants import SmartypantsTest


help_message = """\
--include and --exclude can be used multiple times and both accept a list
of names (names of the test case classes). The order of --include and
--exclude is not significant. Everything listed in --exclude will be filtered
out of the list of tests.

--list output a list of test cases.

Arguments:
    --include [[[TestCase1] TestCase2] ...]
    --exclude [[[TestCase1] TestCase2] ...]
    --list
    --help
"""


def is_test(n):
    return inspect.isclass(n) and issubclass(n, TestCase) and not n is TestCase


def get_tests():
    return inspect.getmembers(sys.modules[__name__], is_test)


def run_tests(include=[], exclude=[]):
    tests = get_tests()

    if include:
        tests = filter(lambda n: n[0] in include, tests)
    if exclude:
        tests = filter(lambda n: not n[0] in exclude, tests)

    runner([n[1] for n in tests])


if __name__ == '__main__':
    include = []
    exclude = []

    if len(sys.argv) >= 2:
        if sys.argv[1] == '--list':
            for name, testcase in get_tests():
                print(name)
            sys.exit(0)
        elif sys.argv[1] == '--help':
            print(help_message)
            sys.exit(0)
        else:
            last_arg = '--include'

            for arg in sys.argv[1:]:
                if arg in ('--include', '--exclude'):
                    last_arg = arg
                elif not arg.startswith('--'):
                    if last_arg == '--include':
                        include.append(arg)
                    elif last_arg == '--exclude':
                        exclude.append(arg)

    run_tests(include, exclude)
