import unittest

from module_05_processes_and_threads.homework.second_block.context_manager import ExceptionContext


def test_function(exc):
    with ExceptionContext(exc) as _:
        c = 2 / 0
    return True


class ContextTests(unittest.TestCase):

    def test_positive(self):
        exc = ZeroDivisionError
        self.assertTrue(test_function(exc))

    def test_negative(self):
        exc = BaseException, Exception
        with self.assertRaises(Exception) as context:
            test_function(exc)
        self.assertTrue(ZeroDivisionError, context.exception)
