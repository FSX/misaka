# -*- coding: utf-8 -*-

"""
chibitest
~~~~~~~~~

chibitest is a simple unit testing module. Less code is less bugs.
Inspired by Oktest, http://www.kuwata-lab.com/oktest/.
"""

from __future__ import print_function

import inspect
import sys
import traceback
from difflib import unified_diff
from collections import defaultdict
from timeit import default_timer


LINE = '*' * 72


def _get_doc_line(obj):
    doc = ''
    if obj.__doc__:
        doc = obj.__doc__.lstrip()
        idx = doc.find('\n')
        if idx > 0:
            doc = doc[:idx]

    return doc


def _exc_name(exception_class):
    if not inspect.isclass(exception_class):
        exception_class = exception_class.__class__

    return '<{}.{}>'.format(
        exception_class.__module__,
        exception_class.__name__)


def readable_duration(s, suffix=''):
    if s >= 1:
        f = '{:.2f} s'.format(s)
    elif s < 1:
        ms = 1000 * s
        if ms >= 1:
            f = '{:.2f} ms'.format(ms)
        elif ms < 1:
            f = '{:.2f} us'.format(ms * 1000)

    return f + suffix


class AssertionObject(object):
    def __init__(self, target):
        self._target = target

    def __lt__(self, other):
        if not self._target < other:
            raise AssertionError('{!r} < {!r}'.format(self._target, other))

    def __le__(self, other):
        if not self._target <= other:
            raise AssertionError('{!r} <= {!r}'.format(self._target, other))

    def __eq__(self, other):
        if not self._target == other:
            raise AssertionError('{!r} == {!r}'.format(self._target, other))

    def __ne__(self, other):
        if not self._target != other:
            raise AssertionError('{!r} != {!r}'.format(self._target, other))

    def __gt__(self, other):
        if not self._target > other:
            raise AssertionError('{!r} > {!r}'.format(self._target, other))

    def __ge__(self, other):
        if not self._target >= other:
            raise AssertionError('{!r} >= {!r}'.format(self._target, other))

    def length(self, other):
        target_length = len(self._target)

        if target_length > other:
            raise AssertionError(
                'Higher than desired length: {!r} > {!r}'
                .format(target_length, other))
        elif target_length < other:
            raise AssertionError(
                'Lower than desired length: {!r} < {!r}'
                .format(target_length, other))

    def diff(self, other):
        if self._target != other:
            difference = unified_diff(
                other.splitlines(True),
                self._target.splitlines(True))
            raise AssertionError(''.join(difference))

    def contains(self, other):
        if other not in self._target:
            raise AssertionError('{!r} in {!r}'.format(other, self._target))

    def not_contains(self, other):
        if other in self._target:
            raise AssertionError('{!r} not in {!r}'.format(other, self._target))

    def raises(self, exception_class=Exception):
        name = _exc_name(exception_class)

        # ``exception_class`` raised. Good!
        # Anything other than ``exception_class`` raised. Wrong!
        # No exception. Wrong!
        try:
            self._target()
        except exception_class:
            pass
        except Exception as e:
            raise AssertionError('Expected {}, but got {}:\n{}'
                                 .format(name, _exc_name(e), e))
        else:
            raise AssertionError('{} not raised'.format(name))

    def not_raises(self, exception_class=Exception):
        name = _exc_name(exception_class)

        # No exception raised. Good!
        # ``exception_class`` raised. Wrong!
        # Any exception raised. Wrong!
        try:
            self._target()
        except exception_class as e:
            raise AssertionError('{} raised:\n{}'.format(name, e))
        except Exception as e:
            raise AssertionError('Expected {} when failing, but got {}:\n{}'
                                 .format(name, _exc_name(e), e))


ok = AssertionObject


class TestResult(object):
    __slots__ = ('func', 'doc_name', 'passed', 'message')

    def __init__(self, func, doc_name=None, passed=False, message=None):
        self.func = func
        self.doc_name = doc_name
        self.passed = passed
        self.message = message

    def name(self):
        return self.doc_name or self.func

    def status(self):
        return 'PASSED' if self.passed else 'FAILED'

    def __str__(self):
        s = '{} ... {}'.format(self.name(), self.status())
        if self.message:
            s += '\n{}\n{}\n{}'.format(LINE, self.message, LINE)

        return s


class BenchmarkResult(TestResult):
    def __init__(self, func, doc_name=None, passed=False, message=None,
            repetitions=0, timing=0.0):
        self.repetitions = repetitions
        self.timing = timing
        TestResult.__init__(self, func, doc_name, passed, message)

    def __str__(self):
        if self.passed:
            s = '{:<25} {:>8} {:>16} {:>16}'.format(
                self.name(),
                self.repetitions,
                readable_duration(self.timing, suffix='/t'),
                readable_duration(self.timing / self.repetitions, suffix='/op'))
        else:
            s = '{} ... FAILED'.format(self.name())

        if self.message:
            s += '\n{}\n{}\n{}'.format(LINE, self.message, LINE)

        return s


class TestCase(object):
    def __init__(self, config):
        self.config = config
        self._tests = []

        for t in dir(self):
            if t.startswith('test_'):
                self.add_test(getattr(self, t))

    @classmethod
    def name(cls):
        name = _get_doc_line(cls)
        if name:
            return '{} ({})'.format(name, cls.__name__)
        else:
            return cls.__name__

    def add_test(self, func):
        self._tests.append(self.wrap_test(func))

    def wrap_test(self, func):
        def catch_exception():
            message = None
            passed = False

            try:
                func()
                passed = True
            except AssertionError as e:  # Expected exception
                message = str(e)
            except Exception as e:  # Unexpected exception
                message = ''.join(traceback.format_exception(
                    *sys.exc_info())).strip()

            return TestResult(
                func.__name__,
                _get_doc_line(func) or None,
                passed,
                message)

        return catch_exception

    def setup(self):
        pass

    def teardown(self):
        pass

    def run(self):
        self.setup()
        for test in self._tests:
            yield test()
        self.teardown()


class Benchmark(TestCase):
    def __init__(self, config):
        self.duration = config.get('duration', 1.0)
        TestCase.__init__(self, config)

    def wrap_test(self, func):
        def catch_exception():
            message = None
            passed = False
            repetitions = 10
            timing = 0.0

            try:
                start = default_timer()
                repeat = 10
                while True:
                    while repeat > 0:
                        func()
                        repeat -= 1

                    if default_timer() - start >= self.duration:
                        break
                    else:
                        repeat = 10
                        repetitions += 10

                timing = default_timer() - start
                passed = True
            except AssertionError as e:  # Expected exception
                message = str(e)
            except Exception as e:  # Unexpected exception
                message = ''.join(traceback.format_exception(
                    *sys.exc_info())).strip()

            return BenchmarkResult(
                func.__name__,
                _get_doc_line(func) or None,
                passed,
                message,
                repetitions,
                timing)

        return catch_exception


def runner(testcases, setup_func=None, teardown_func=None, config={}):
    passed = failed = 0
    config = defaultdict(lambda: None, config)

    if setup_func:
        setup_func()

    for testcase in testcases:
        tests = testcase(config)

        print('>> {}'.format(testcase.name()))

        for result in tests.run():
            if result.passed:
                passed += 1
            else:
                failed += 1
            print(result)

        print()

    if teardown_func:
        teardown_func()

    print('{} passed; {} failed.'.format(passed, failed))
    if failed > 0:
        sys.exit(1)
