"""
Simple Representation module.

This module provide utility methods and mixin to convert python objects
to and from a so called 'simple representation'.

A simple representation is composed only of simple python objects:
* booleans
* string
* numbers
* lists of simple python objects
* dicts of simple python objects
* namedtuple

When using namedtuple, they must obey the two following rules
* be defined at module level (not in class /method)
* the name of the class variable must match the name of the class. for
  example:

    Named = namedtuple('Named', ['foo', 'bar'])


"""


class SimpleReprException(Exception):
    pass

