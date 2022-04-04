import pytest

from pacman.dcop.objects import Domain, Variable, create_variables
from pacman.utils.simple_repr import from_repr, simple_repr


class TestDomain:
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

    def test_raises_when_no_domain(self):
        with pytest.raises(TypeError):
            Variable("v")

    def test_no_initial_value(self):
        v = Variable("v", [1, 2, 3, 4])
        assert v.initial_value is None

    def test_initial_value(self):
        v = Variable("v", [1, 2, 3, 4], 1)
        assert v.initial_value == 1

    def test_invalid_initial_value(self):
        with pytest.raises(ValueError):
            Variable("v", [1, 2, 3, 4], "A")
            Variable("v", [1, 2, 3, 4], initial_value="A")

    def test_simple_repr(self):
        d = Domain("d", "foo", [1, 2, 3])
        v = Variable("v", d, 2)
        r = simple_repr(v)
        assert r["name"] == "v"
        assert r["domain"] == simple_repr(d)
        assert r["initial_value"] == 2

    def test_simple_repr_no_initial_value(self):
        d = Domain("d", "foo", [1, 2, 3])
        v = Variable("v", d)
        r = simple_repr(v)
        assert r["name"] == "v"
        assert r["domain"] == simple_repr(d)
        assert r["initial_value"] is None

    def test_simple_repr_list_based_domain(self):
        v = Variable("v", [1, 2, 3, 4])
        r = simple_repr(v)
        assert r["name"] == "v"
        assert r["initial_value"] is None
        assert r["domain"] == simple_repr(v.domain)
        assert 1 in r["domain"]["values"]
        assert r["domain"]["values"]["__qualname__"] == "tuple"

    def test_from_simple_repr(self):
        d = Domain("d", "foo", [1, 2, 3])
        v = Variable("v", d, 2)
        r = simple_repr(v)
        v2 = from_repr(r)
        assert v2 == v

    def test_hash(self):
        d = Domain("d", "foo", [1, 2, 3])
        v1 = Variable("v", d, 2)
        v2 = Variable("v", d, 2)
        v3 = Variable("v", d, 3)
        h1 = hash(v1)
        h2 = hash(v2)
        h3 = hash(v3)
        assert h1 == h2
        assert h1 != h3


class TestCreateVariables:
    def test_create_variables_from_list(self):
        d = Domain("d", "foo", [1, 2, 3])
        variables = create_variables("x_", ["a1", "a2", "a3"], d)
        assert "x_a1" in variables
        assert isinstance(variables["x_a1"], Variable)
        assert variables["x_a1"].name == "x_a1"

    def test_create_variables_from_range(self):
        d = Domain("d", "foo", [1, 2, 3])
        variables = create_variables("x_", range(3), d)
        assert "x_0" in variables
        assert isinstance(variables["x_0"], Variable)
        assert variables["x_0"].name == "x_0"

    def test_create_variables_from_lists(self):
        d = Domain("d", "foo", [1, 2, 3])
        variables = create_variables("x_", (["a1", "a2", "a3"], ["b1", "b2", "b3"]), d)
        assert ("a1", "b2") in variables
        assert isinstance(variables[("a1", "b2")], Variable)
        assert variables[("a1", "b2")].name == "x_a1_b2"
