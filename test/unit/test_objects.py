import pytest

from pacman.dcop.objects import Domain, Variable
from pacman.utils.simple_repr import simple_repr, from_repr


class TestVariableDomain:
    def test_simple_repr(self):
        d = Domain("d", "foo", [1, 2, 3])
        r = simple_repr(d)
        print(r)
        assert r["__qualname__"] == "Domain"
        assert r["__module__"] == "pacman.dcop.objects"
        assert r["name"] == "d"
        assert r["domain_type"] == "foo"

    def test_from_simple_repr(self):
        d = Domain("d", "foo", [1, 2, 3])
        r = simple_repr(d)
        d2 = from_repr(r)

        assert d2 == d

    def test_hash(self):
        d1 = Domain("d", "foo", [1, 2, 3])
        d2 = Domain("d", "foo", [1, 2, 3])
        d3 = Domain("d", "foo", [1, 2, 4])
        h1 = hash(d1)
        h2 = hash(d2)
        h3 = hash(d3)
        assert h1 == h2
        assert h1 != h3

class TestVariable:
    def test_list_domain(self):
        v = Variable("v", [1, 2, 3, 4])
        assert isinstance(v.domain, Domain)


