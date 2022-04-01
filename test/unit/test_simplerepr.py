from pacman.utils.simple_repr import SimpleRepr, from_repr


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
        r = a.__simple_repr()

        assert r['attr1'] == 'foo'
        assert r['attr2'] == 'bar'

    def test_simple_attr_only_with_bool(self):
        a = A(False, True)
        r = a.__simple_repr()

        assert r['attr1'] is False
        assert r['attr2'] is True

    def test_simple_attr_only_with_none(self):
        a = A(False, None)
        r = a.__simple_repr()

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
