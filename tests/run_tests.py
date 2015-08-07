# -*- coding: utf-8 -*-

import importlib
import inspect
import os
import sys
from itertools import chain
from os.path import dirname, join as jp, splitext

CWD = dirname(sys.modules[__name__].__file__)
sys.path.insert(0, jp(CWD, '..'))

from chibitest import runner, TestCase


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


def get_test_modules():
    modules = []

    for n in os.listdir(CWD):
        if n.startswith('test_') and n.endswith('.py'):
            n, _ = splitext(n)
            modules.append(importlib.import_module(n))

    return modules


def is_test(n):
    return inspect.isclass(n) and issubclass(n, TestCase) and not n is TestCase


def get_tests(module):
    return [(testcase.name(), testcase) \
        for _, testcase in inspect.getmembers(module, is_test)]


def run_tests(tests, include=[], exclude=[]):
    if include:
        tests = [n for n in tests if n[0] in include]
    if exclude:
        tests = [n for n in tests if not n[0] in exclude]

    runner([n[1] for n in tests])


if __name__ == '__main__':
    tests = list(chain(*map(get_tests, get_test_modules())))
    include = []
    exclude = []

    if len(sys.argv) >= 2:
        if sys.argv[1] == '--list':
            for name, testcase in tests:
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

    run_tests(tests, include, exclude)
