import pytest

from pacman.utils.various import func_args
# from pacman.utils.expressionfunction import ExpressionFunction


class TestFuncArgs:

    def test_one_arg(self):
        def f(a):
            return a * 2

        var_list = func_args(f)

        assert var_list == ['a']

    def test_two_arg(self):
        def f(a, b):
            return a + b

        var_list = func_args(f)

        assert var_list == ['a', 'b']

    def test_one_partial(self):
        def f(a, b, c):
            return a + b

        var_list = func_args(f)
        assert var_list == ['a', 'b', 'c']

        from functools import partial
        f2 = partial(f, b=2)

        var_list = func_args(f2)
        assert var_list == ['a', 'c']

    def test_one_partial_twice(self):
        def f(a, b, c):
            return a + b

        var_list = func_args(f)
        assert var_list == ['a', 'b', 'c']

        from functools import partial
        f2 = partial(f, b=2)
        f3 = partial(f2, a=2)

        var_list = func_args(f3)
        assert var_list == ['c']

    def test_lambda(self):
        f = lambda a, b: a + b

        var_list = func_args(f)

        assert var_list == ['a', 'b']

    # def test_expression_function(self):
    #     f = ExpressionFunction('a + b + v1')
    #     var_list = func_args(f)
    #
    #     assert 'a' in var_list
    #     assert 'b' in var_list
    #     assert 'v1' in var_list
    #     assert len(var_list), 3
