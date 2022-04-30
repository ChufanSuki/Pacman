import pytest

from pacman.dcop.relations import ZeroAryRelation
from pacman.utils.simple_repr import from_repr, simple_repr


@pytest.fixture
def zero_arity_relation():
    return ZeroAryRelation("r0", 42)


class TestZeroAryRelation:
    def test_properties(self, zero_arity_relation):
        assert zero_arity_relation.name == "r0"
        assert zero_arity_relation.dimensions == []
        assert zero_arity_relation.arity == 0
        assert zero_arity_relation.shape == ()

    def test_get_value(self, zero_arity_relation):
        assert zero_arity_relation() == 42
        assert zero_arity_relation.get_value_for_assignment([]) == 42
        with pytest.raises(ValueError):
            zero_arity_relation.get_value_for_assignment(["x1"])
        with pytest.raises(ValueError):
            zero_arity_relation(["x1"], ["a"])

    def test_set_value(self, zero_arity_relation):
        r1 = zero_arity_relation.set_value_for_assignment({}, 21)
        assert r1() == 21

    def test_slicing_on_no_var_is_ok(self, zero_arity_relation):
        r1 = zero_arity_relation.slice({})
        assert r1() == 42

    def test_slicing_on_variable_raises_valueerror(self, zero_arity_relation):
        with pytest.raises(ValueError):
            zero_arity_relation.slice({"x1": "a"})

    def test_set_value_for_assignment(self, zero_arity_relation):
        r1 = zero_arity_relation.set_value_for_assignment({}, 21)
        assert r1() == 21
        assert hash(r1) != hash(zero_arity_relation)
        assert id(r1) != id(zero_arity_relation)

    def test_simple_repr(self, zero_arity_relation):
        r = simple_repr(zero_arity_relation)
        assert r["name"] == "r0"
        assert r["value"] == 42

    def test_from_repr(self, zero_arity_relation):
        r = simple_repr(zero_arity_relation)
        r1 = from_repr(r)
        assert r1() == 42
        assert hash(r1) == hash(zero_arity_relation)
        assert r1 == zero_arity_relation

    def test_hash(self, zero_arity_relation):
        h = hash(zero_arity_relation)
        assert h is not None
        assert h == hash(ZeroAryRelation("r0", 42))
        assert h != hash(ZeroAryRelation("r1", 42))
        assert h != hash(ZeroAryRelation("r0", 43))
