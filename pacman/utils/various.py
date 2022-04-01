def func_args(f):
    """
    Get the list of arguments for a function.
    This also works for function produced with functools.partial, as long as
    you only use keywords arguments.

    :param f: a function
    :return: the list of argument's name for the function f
    """
    try:
        # get argument list using code object of f
        return list(f.__code__.co_varnames[:f.__code__.co_argcount])
    except AttributeError:

        if hasattr(f, 'variable_names'):
            return f.variable_names

        original_args = func_args(f.func)

        var_list = [a for a in original_args if a not in f.keywords]
        return var_list
