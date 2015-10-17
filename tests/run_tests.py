# -*- coding: utf-8 -*-

import importlib
import inspect
import os
import sys
from itertools import chain
from os.path import dirname, join as jp, splitext

CWD = dirname(sys.modules[__name__].__file__)
sys.path.insert(0, jp(CWD, '..'))

from chibitest import runner, TestCase, Benchmark


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


def is_testcase(n):
    return inspect.isclass(n) \
        and issubclass(n, TestCase) \
        and not n is TestCase \
        and not n is Benchmark


def is_benchmark(n):
    return inspect.isclass(n) \
        and issubclass(n, Benchmark) \
        and not n is Benchmark


def get_testcases(module):
    return [(testcase.name(), testcase) \
        for _, testcase in inspect.getmembers(module, is_testcase)]


def run_testcases(testcases, include=[], exclude=[]):
    if include:
        testcases = [n for n in testcases if n[0] in include]
    if exclude:
        testcases = [n for n in testcases if not n[0] in exclude]

    runner([n[1] for n in testcases])


if __name__ == '__main__':
    testcases = list(chain(*map(get_testcases, get_test_modules())))
    include = []
    exclude = []

    if len(sys.argv) >= 2:
        if sys.argv[1] == '--list':
            for name, testcase in testcases:
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

    if '--benchmark' in sys.argv[1:]:
        testcases = list(filter(lambda n: is_benchmark(n[1]), testcases))
    else:
        testcases = list(filter(lambda n: not is_benchmark(n[1]), testcases))

    run_testcases(testcases, include, exclude)
