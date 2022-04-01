from collections import namedtuple

import pytest

from pacman.utils.simple_repr import SimpleRepr, from_repr, SimpleReprException, simple_repr


class A(SimpleRepr):
    def __init__(self, attr1, attr2):
        self._attr1 = attr1
        self._attr2 = attr2


class TestAttrHaveSameNameAsInitParams:
    """
    Tests for the case where all attributes in the class maps directly to
    argument of the __init__ constructor:

    e.g.

    A.__init__(a) --> A._a
    """

    def test_simple_attr_only(self):
        a = A('foo', 'bar')
        r = a._simple_repr()

        assert r['attr1'] == 'foo'
        assert r['attr2'] == 'bar'

    def test_simple_attr_only_with_bool(self):
        a = A(False, True)
        r = a._simple_repr()

        assert r['attr1'] is False
        assert r['attr2'] is True

    def test_simple_attr_only_with_none(self):
        a = A(False, None)
        r = a._simple_repr()

        assert r['attr1'] is False
        assert r['attr2'] is None

    def test_from_repr_simple_attr_only(self):
        a = A('foo', 'bar')
        r = a._simple_repr()

        b = from_repr(r)
        assert isinstance(b, A) is True
        assert b._attr1 == 'foo'
        assert b._attr2 == 'bar'

    def test_list_attr(self):
        a = A('foo', [1, 2, 3])
        r = a._simple_repr()

        assert r['attr1'] == 'foo'
        assert r['attr2'] == [1, 2, 3]

    def test_from_repr_list_attr(self):
        a = A('foo', [1, 2, 3])
        r = a._simple_repr()

        b = from_repr(r)
        assert b._attr1 == a._attr1
        assert b._attr2 == a._attr2

    def test_dict_attr(self):
        a = A('foo', {'a': 1, 'b': 2})
        r = a._simple_repr()

        assert r['attr1'] == 'foo'
        assert r['attr2'] == {'a': 1, 'b': 2}

    def test_from_repr_dist_attr(self):
        a = A('foo', {'a': 1, 'b': 2})
        r = a._simple_repr()

        b = from_repr(r)
        assert b._attr1 == a._attr1
        assert b._attr2 == a._attr2

    def test_object_attr(self):
        a2 = A('foo2', 'bar2')
        a = A('foo', a2)
        r = a._simple_repr()

        assert r['attr1'] == 'foo'
        assert r['attr2'] == a2._simple_repr()
        assert r['attr2']['attr1'] == 'foo2'

    def test_from_repr_object_attr(self):
        a2 = A('foo2', 'bar2')
        a = A('foo', a2)
        r = a._simple_repr()

        b = from_repr(r)
        assert isinstance(b, A) is True
        assert b._attr1 == 'foo'
        assert b._attr2._attr1 == 'foo2'
        assert b._attr2._attr2 == 'bar2'

    def test_list_of_objects(self):
        a2 = A('foo2', 'bar2')
        a3 = A('foo3', 'bar3')
        a = A('foo', [a2, a3])
        r = a._simple_repr()

        assert r['attr1'] == 'foo'
        assert isinstance(r['attr2'], list) is True
        assert r['attr2'][0] == a2._simple_repr()
        assert r['attr2'][1]['attr1'] == 'foo3'

    def test_from_repr_list_of_objects(self):
        a2 = A('foo2', 'bar2')
        a3 = A('foo3', 'bar3')
        a = A('foo', [a2, a3])
        r = a._simple_repr()

        b = from_repr(r)
        assert isinstance(b, A) is True
        assert b._attr1 == 'foo'
        assert isinstance(b._attr2, list) is True
        assert b._attr2[0]._attr1 == 'foo2'
        assert b._attr2[1]._attr2 == 'bar3'

    def test_dict_of_objects(self):
        a2 = A('foo2', 'bar2')
        a3 = A('foo3', 'bar3')
        a = A('foo', {'a': a2, 'b': a3})
        r = a._simple_repr()
        assert r['attr1'] == 'foo'
        assert isinstance(r['attr2'], dict) is True
        assert r['attr2']['a'] == a2._simple_repr()
        assert r['attr2']['b']['attr1'] == 'foo3'

    def test_composite_list_dict(self):
        a2 = A('foo2', 'bar2')
        a = A('foo', ['a', {'k1': 1, 'k2': a2}, 3])
        r = a._simple_repr()
        assert r['attr1'] == 'foo'
        assert isinstance(r['attr2'], list) is True
        assert isinstance(r['attr2'][1], dict) is True
        assert r['attr2'][1]['k2']['attr2'] == 'bar2'

    def test_raise_when_object_does_not_use_mixin(self):
        class NoMixin(object):

            def __init__(self, a1):
                self.foo = a1

        o = NoMixin('bar')
        with pytest.raises(SimpleReprException):
            simple_repr(o)

    def test_raise_when_no_corresponding_attribute(self):
        class NoCorrespondingAttr(SimpleRepr):

            def __init__(self, a1):
                self.foo = a1

        o = NoCorrespondingAttr('bar')
        with pytest.raises(SimpleReprException):
            simple_repr(o)

    def test_mapping_for_corresponding_attribute(self):
        class MappingAttr(SimpleRepr):

            def __init__(self, a1):
                self._repr_mapping = {'a1': 'foo'}
                self.foo = a1

        o = MappingAttr('bar')
        r = simple_repr(o)
        assert r['a1'] == 'bar'

    def test_tuple_simple_repr(self):
        a1 = A('foo', ('b', 'a'))
        r = simple_repr(a1)
        print(r)

    def test_tuple_from_repr(self):
        a1 = A('foo', ('b', 'a'))
        r = simple_repr(a1)
        a2 = from_repr(r)
        print(a2)

    def test_namedtuple(self):
        # Named = namedtuple('Named', ['foo', 'bar'])
        n = Named(1, 2)
        r = simple_repr(n)

        self.assertEqual(r['foo'], 1)
        self.assertEqual(r['bar'], 2)

        obtained = from_repr(r)

        self.assertEqual(obtained, n)

    def test_namedtuple_complex(self):
        # Named = namedtuple('Named', ['foo', 'bar'])
        n = Named({'a': 1, 'b': 2}, [1, 2, 3, 5])
        r = simple_repr(n)

        self.assertEqual(r['foo'], {'a': 1, 'b': 2})
        self.assertEqual(r['bar'], [1, 2, 3, 5])

        obtained = from_repr(r)

        self.assertEqual(obtained, n)


Named = namedtuple('Named', ['foo', 'bar'])
