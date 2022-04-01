import unittest

from pacman.utils.various import func_args
from pacman.utils.expressionfunction import ExpressionFunction


class FuncArgsTests(unittest.TestCase):

    def test_one_arg(self):
        def f(a):
            return a * 2

        var_list = func_args(f)

        self.assertEqual(var_list, ['a'])

    def test_two_arg(self):
        def f(a, b):
            return a + b

        var_list = func_args(f)

        self.assertEqual(var_list, ['a', 'b'])

    def test_one_partial(self):
        def f(a, b, c):
            return a + b

        var_list = func_args(f)
        self.assertEqual(var_list, ['a', 'b', 'c'])

        from functools import partial
        f2 = partial(f, b=2)

        var_list = func_args(f2)
        self.assertEqual(var_list, ['a', 'c'])

    def test_one_partial_twice(self):
        def f(a, b, c):
            return a + b

        var_list = func_args(f)
        self.assertEqual(var_list, ['a', 'b', 'c'])

        from functools import partial
        f2 = partial(f, b=2)
        f3 = partial(f2, a=2)

        var_list = func_args(f3)
        self.assertEqual(var_list, ['c'])

    def test_lambda(self):
        f = lambda a, b: a + b

        var_list = func_args(f)

        self.assertEqual(var_list, ['a', 'b'])

    def test_expression_function(self):
        f = ExpressionFunction('a + b + v1')
        var_list = func_args(f)

        self.assertIn('a', var_list)
        self.assertIn('b', var_list)
        self.assertIn('v1', var_list)
        self.assertEqual(len(var_list), 3)
