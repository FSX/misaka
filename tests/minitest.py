import re
import sys
from difflib import unified_diff
from collections import namedtuple


RE_TEST_NAME = re.compile(r'test_[a-zA-Z0-9_]*')
Result = namedtuple('Result', ('func', 'name', 'error'))


def msg(message):
    return '{0}\n{1}\n{0}'.format('-' * 80, message)


class ExtendedDict(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            return None

    def __setattr__(self, name, value):
        self[name] = value


class AssertionObject(object):
    def __init__(self, target):
        self._target = target

    def __lt__(self, other):
        if not self._target < other:
            raise AssertionError(msg('%r < %r' % (self._target, other)))

    def __le__(self, other):
        if not self._target <= other:
            raise AssertionError(msg('%r <= %r' % (self._target, other)))


    def __eq__(self, other):
        if not self._target == other:
            raise AssertionError(msg('%r == %r' % (self._target, other)))

    def __ne__(self, other):
        if not self._target != other:
            raise AssertionError(msg('%r != % ' % (self._target, other)))

    def __gt__(self, other):
        if not self._target > other:
            raise AssertionError(msg('%r > %r' % (self._target, other)))

    def __ge__(self, other):
        if not self._target >= other:
            raise AssertionError(msg('%r >= %r' % (self._target, other)))

    def diff(self, other):
        if self._target != other:
            difference = unified_diff(
                other.splitlines(True),
                self._target.splitlines(True))
            raise AssertionError(msg(''.join(difference)))

    def contains(self, other):
        if other not in self._target:
            raise AssertionError(msg('%r in %r' % (other, self._target)))

    def not_contains(self, other):
        if other in self._target:
            raise AssertionError(msg('%r not in %r' % (other, self._target)))


def ok(target):
    return AssertionObject(target)


class TestCase(object):
    def __init__(self, config):
        self.config = config
        self._tests = []
        for t in dir(self):
            if RE_TEST_NAME.match(t):
                self.add_test(getattr(self, t))

    def add_test(self, func):
        def catch_exception():
            try:
                func()
                error = None
            except AssertionError as e:
                error = str(e)
            return Result(func.__name__, func.__doc__, error)
        self._tests.append(catch_exception)
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


def runner(testcases, config={}):
    passed = failed = 0
    config = ExtendedDict(config)

    for testcase in testcases:
        tests = testcase(config)

        if hasattr(tests, 'name'):
            print('\n>> %s' % tests.name)

        for result in tests.run():
            name = result.name or result.func
            if result.error is not None:
                failed += 1
                print('%s ... FAILED\n\n%s\n' % (name, result.error))
            else:
                passed += 1
                print('%s ... PASSED' % name)

    print('\n\n%s passed; %s failed.' % (passed, failed))
