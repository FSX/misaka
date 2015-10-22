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
Options:
  --include (-i)    comma separated list of testcases
  --exclude (-e)    comma separated list of testcases
  --benchmark (-b)  run bechmarks
  --list (-l)       list all testcases
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
    return [(testcase.__name__, testcase) \
        for _, testcase in inspect.getmembers(module, is_testcase)]


def run_testcases(testcases, benchmark=False, include=[], exclude=[]):
    if include:
        testcases = [n for n in testcases if n[0] in include]
    if exclude:
        testcases = [n for n in testcases if not n[0] in exclude]

    if benchmark:
        testcases = [n[1] for n in testcases if is_benchmark(n[1])]
    else:
        testcases = [n[1] for n in testcases if not is_benchmark(n[1])]

    runner(testcases)


if __name__ == '__main__':
    testcases = list(chain(*map(get_testcases, get_test_modules())))
    include = []
    exclude = []
    benchmark = False

    if len(sys.argv) >= 2:
        if sys.argv[1] in ('-l', '--list'):
            for name, testcase in testcases:
                print(name)
            sys.exit(0)
        elif sys.argv[1] in ('-h', '--help'):
            print(help_message)
            sys.exit(0)
        else:
            last_arg = '--include'
            for arg in sys.argv[1:]:
                if arg in ('-i', '--include', '-e', '--exclude'):
                    last_arg = arg
                elif not arg.startswith('-'):  # - or --
                    arg = [n for n in arg.split(',') if n]
                    if last_arg in ('-i', '--include'):
                        include.extend(arg)
                    elif last_arg in ('-e', '--exclude'):
                        exclude.extend(arg)

    if '-b' in sys.argv[1:] or '--benchmark' in sys.argv[1:]:
        benchmark = True

    run_testcases(testcases, benchmark, include, exclude)
