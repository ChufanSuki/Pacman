from collections.abc import Callable


class ExpressionFunction(Callable, SimpleRepr):
    """
    Callable object representing a function from a python string.
    expression.

    Example:
    f = ExpressionFunction('a + b')
    f.variable_names  -> ['a', 'b']
    f(a=1, b=3)       -> 4
    f.expression      -> 'a + b'

    Note: this callable only works with keyword arguments.

    """

    def __init__(self, expression: str, source_file=None, **fixed_vars) -> None:
        """
        Create a callable representing the expression.

        :param expression: a valid python expression (any builtin python
        function can be used, e.g. abs, round, etc.).
        for example "abs(a1 - b)"

        :param fixed_vars: extra keyword parameters will be interpreted as
        fixed parameter for the expression and the produced callable will
        represent a partial evaluation if the expression with these
        parameter already fixed. If the name of these keyword parameter do
        not match any of the variables found in the expression,
        a `ValueError` is raised.
        """