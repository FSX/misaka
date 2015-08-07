# -*- coding: utf-8 -*-

"""
chibitest
~~~~~~~~~

chibitest is a simple unit testing module. Less code is less bugs.
Inspired by Oktest, http://www.kuwata-lab.com/oktest/.
"""

from __future__ import print_function

import sys
import inspect
import traceback
from difflib import unified_diff
from collections import namedtuple, defaultdict


Result = namedtuple('Result', ('func', 'name', 'failure'))


def _exc_name(exception_class):
    if not inspect.isclass(exception_class):
        exception_class = exception_class.__class__

    return '<{}.{}>'.format(
        exception_class.__module__,
        exception_class.__name__)


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
            raise AssertionError('Higher than desired length: {!r} > {!r}'
                .format(target_length, other))
        elif target_length < other:
            raise AssertionError('Lower than desired length: {!r} < {!r}'
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


# A nicer alias.
ok = AssertionObject


class TestCase(object):
    def __init__(self, config):
        self.config = config
        self._tests = []

        for t in dir(self):
            if t.startswith('test_'):
                self._tests.append(self._wrap_test(getattr(self, t)))

    def add_test(self, func):
        self._tests.append(self._wrap_test(func))

    def _wrap_test(self, func):
        def catch_exception():
            failure = None

            try:
                func()
            except AssertionError as e:
                failure = str(e)
            except Exception as e:
                failure = ''.join(traceback.format_exception(
                    *sys.exc_info())).strip()

            doc = ''
            if func.__doc__:
                doc = func.__doc__.lstrip()
                idx = doc.find('\n')
                if idx > 0:
                    doc = doc[:idx]

            return Result(func.__name__, doc or None, failure)

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


def runner(testcases, setup_func=None, teardown_func=None, config={}):
    line = '*' * 80
    passed = failed = 0
    config = defaultdict(lambda: None, config)

    if setup_func:
        setup_func()

    for testcase in testcases:
        tests = testcase(config)

        print('>> {}'.format(tests.name if hasattr(tests, 'name')
              else testcase.__name__))

        for result in tests.run():
            name = result.name or result.func
            if result.failure is not None:
                failed += 1

                if result.failure:
                    print('{} ... FAILED\n{}\n{}\n{}'
                        .format(name, line, result.failure, line))
                else:
                    print('{} ... FAILED'.format(name))
            else:
                passed += 1
                print('{} ... PASSED'.format(name))

        print()

    if teardown_func:
        teardown_func()

    print('{} passed; {} failed.'.format(passed, failed))
    if failed > 0:
        sys.exit(1)
