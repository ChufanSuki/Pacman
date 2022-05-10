
from pacman.algorithms import ComputationDef, AlgorithmDef
from pacman.algorithms.maxsum import (
    MaxSumVariableComputation,
    MaxSumFactorComputation,
    build_computation,
    factor_costs_for_var,
    select_value,
)
from pacman.computations_graph.factor_graph import build_computation_graph
from pacman.dcop.objects import (
    Variable,
    Domain,
    VariableWithCostDict,
    VariableWithCostFunc,
)
from pacman.dcop.relations import constraint_from_str


def test_comp_creation():
    d = Domain("d", "", ["R", "G"])
    v1 = Variable("v1", d)
    v2 = Variable("v2", d)
    c1 = constraint_from_str("c1", "10 if v1 == v2 else 0", [v1, v2])
    graph = build_computation_graph(None, constraints=[c1], variables=[v1, v2])

    comp_node = graph.computation("c1")
    algo_def = AlgorithmDef.build_with_default_param("maxsum")
    comp_def = ComputationDef(comp_node, algo_def)

    comp = MaxSumFactorComputation(comp_def)
    assert comp is not None
    assert comp.name == "c1"
    assert comp.factor == c1

    comp_node = graph.computation("v1")
    algo_def = AlgorithmDef.build_with_default_param("maxsum")
    comp_def = ComputationDef(comp_node, algo_def)

    comp = MaxSumVariableComputation(comp_def)
    assert comp is not None
    assert comp.name == "v1"
    assert comp.variable.name == "v1"
    assert comp.factors == ["c1"]


def test_comp_creation_with_factory_method():
    d = Domain("d", "", ["R", "G"])
    v1 = Variable("v1", d)
    v2 = Variable("v2", d)
    c1 = constraint_from_str("c1", "10 if v1 == v2 else 0", [v1, v2])
    graph = build_computation_graph(None, constraints=[c1], variables=[v1, v2])

    comp_node = graph.computation("c1")
    algo_def = AlgorithmDef.build_with_default_param("maxsum")
    comp_def = ComputationDef(comp_node, algo_def)

    comp = build_computation(comp_def)
    assert comp is not None
    assert comp.name == "c1"
    assert comp.factor == c1

    comp_node = graph.computation("v1")
    algo_def = AlgorithmDef.build_with_default_param("maxsum")
    comp_def = ComputationDef(comp_node, algo_def)

    comp = build_computation(comp_def)
    assert comp is not None
    assert comp.name == "v1"
    assert comp.variable.name == "v1"
    assert comp.factors == ["c1"]


def test_compute_factor_cost_at_start():
    d = Domain("d", "", ["R", "G"])
    v1 = Variable("v1", d)
    v2 = Variable("v2", d)
    c1 = constraint_from_str("c1", "10 if v1 == v2 else 0", [v1, v2])

    obtained = factor_costs_for_var(c1, v1, {}, "min")
    assert obtained["R"] == 0
    assert obtained["G"] == 0
    assert len(obtained) == 2


def test_select_value_no_cost_var():
    d = Domain("d", "", ["R", "G", "B"])
    v1 = Variable("v1", d)

    selected, cost = select_value(v1, {}, "min")
    assert selected in {"R", "G", "B"}
    assert cost == 0

    v1 = VariableWithCostFunc("v1", [1, 2, 3], lambda v: (4 - v) / 10)

    selected, cost = select_value(v1, {}, "min")
    assert selected == 3
    assert cost == 0.1
