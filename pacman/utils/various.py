def func_args(f):
    """
    Get the list of arguments for a function.
    This also works for function produced with functools.partial, as long as
    you only use keywords arguments.

    :param f: a function
    :return: the list of argument's name for the function f
    """