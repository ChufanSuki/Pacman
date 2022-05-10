

from pacman.algorithms import (
    AlgorithmDef,
    list_available_algorithms,
    load_algorithm_module,
)
from pacman.utils.simple_repr import simple_repr, from_repr


def test_algo_def():

    a = AlgorithmDef("maxsum", {"stability": 0.01}, "min")

    assert a.algo == "maxsum"
    assert a.mode == "min"
    assert "stability" in a.param_names()
    assert a.param_value("stability") == 0.01


def test_simple_repr():

    a = AlgorithmDef("maxsum", {"stability": 0.01}, "min")

    r = simple_repr(a)

    assert r["algo"] == "maxsum"
    assert r["mode"] == "min"
    assert r["params"]["stability"] == 0.01


def test_from_repr():

    a = AlgorithmDef("maxsum", {"stability": 0.01}, "min")

    r = simple_repr(a)
    a2 = from_repr(r)

    assert a == a2
    assert a2.param_value("stability") == 0.01


def test_building_algodef_with_default_params():

    a = AlgorithmDef.build_with_default_param("amaxsum")

    assert a.params["damping"] == 0.5


def test_building_algodef_with_provided_and_default_params():

    a = AlgorithmDef.build_with_default_param("dsa", {"variant": "B"}, mode="max")

    assert a.params["variant"] == "B"  # provided param
    assert a.params["probability"] == 0.7  # default param
    assert a.algo == "dsa"
    assert a.mode == "max"


def test_load_algorithm():

    # We test load for all available algorithms
    for a in list_available_algorithms():
        algo = load_algorithm_module(a)

        assert algo.algorithm_name == a
        assert hasattr(algo, "communication_load")
        assert hasattr(algo, "computation_memory")


def test_load_algorithm_with_default_footprint():

    # dsatuto has no load method defined : check that we get instead default
    # implementations
    algo = load_algorithm_module("dsatuto")
    assert algo.algorithm_name == "dsatuto"
    assert algo.communication_load(None, None) == 1
    assert algo.computation_memory(None) == 1
