from functools import partial

import pytest

from pacman.utils.expressionfunction import ExpressionFunction


class TestExpressionFunction:
    def test_callable(self):
        f = ExpressionFunction('a / b ')
        assert f(a=1, b=2) == 0.5

    def test_simple_math_expression(self):
        f = ExpressionFunction('a + b ')
        assert f.expression == 'a + b '

    def test_oneline_python_expression(self):
        f = ExpressionFunction(' "ko" if a+b > 10 else a+b')

        assert f(a=2, b=3) == 5
        assert f(a=4, b=8) == "ko"

    def test_complex_oneline_exp(self):
        # This kind of expression is exactly what we use when modelling an
        # hard constraint:
        f = ExpressionFunction('0 if round(0.2*a + 0.5*b + 0.8*c) == M '
                               'else 1000')

        assert f(a=10, b=10, c=10, M=15) == 0
        assert f(a=10, b=10, c=10, M=13) == 1000
        assert f(a=5, b=2, c=3, M=4) == 0

    def test_variable_names(self):
        f = ExpressionFunction('a + b ')
        names = f.variable_names

        assert len(list(names)) == 2
        assert 'a' in names
        assert 'b' in names

    def test_should_work_with_partial(self):
        f = ExpressionFunction('a * (b -c)')

        fp = partial(f, c=2)
        assert f(a=2, b=5, c=2) == 6
        assert f(a=2, b=5, c=2) == fp(a=2, b=5)

        fp = partial(f, c=1, a=3)
        assert f(a=3, b=5, c=1) == fp(b=5)

    def test_non_numeric_variable(self):
        f = ExpressionFunction("1 if a == 'A' else 2")
        assert f(a='A') == 1
        assert f(a='B') == 2

    def test_str_with_function_call(self):
        r = ExpressionFunction('abs(s1 - s2)')

        assert len(list(r.variable_names)) == 2
        assert r(s1=2, s2=3) == 1
        assert r(s1=3, s2=2) == 1

    def test_raise_on_syntax_error(self):
        with pytest.raises(SyntaxError):
            ExpressionFunction('(s1 - s2')
