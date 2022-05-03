
from unittest.mock import MagicMock, call

from pacman.algorithms import dsa, AlgorithmDef, ComputationDef
from pacman.algorithms.dsa import DsaComputation, DsaMessage
from pacman.computations_graph.constraints_hypergraph \
    import VariableComputationNode
from pacman.dcop.objects import Variable
from pacman.dcop.relations import UnaryFunctionRelation, \
    AsNAryFunctionRelation, relation_from_str, constraint_from_str


def test_communication_load():
    v = Variable('v1', list(range(10)))
    var_node = VariableComputationNode(v, [])
    assert dsa.UNIT_SIZE + dsa.HEADER_SIZE == dsa.communication_load(
        var_node, 'f1')


def test_computation_memory_one_constraint():
    v1 = Variable('v1', list(range(10)))
    v2 = Variable('v2', list(range(10)))
    v3 = Variable('v3', list(range(10)))
    c1 = constraint_from_str('c1', ' v1 + v2 == v3', [v1, v2, v3])
    v1_node = VariableComputationNode(v1, [c1])

    # here, we have a hyper-edges with 3 vertices
    assert dsa.computation_memory(v1_node) == dsa.UNIT_SIZE * 2


def test_computation_memory_two_constraints():
    v1 = Variable('v1', list(range(10)))
    v2 = Variable('v2', list(range(10)))
    v3 = Variable('v3', list(range(10)))
    v4 = Variable('v4', list(range(10)))
    c1 = constraint_from_str('c1', ' v1 == v2', [v1, v2])
    c2 = constraint_from_str('c2', ' v1 == v3', [v1, v3])
    c3 = constraint_from_str('c3', ' v1 == v4', [v1, v4])
    v1_node = VariableComputationNode(v1, [c1, c2, c3])

    # here, we have 3 edges , one for each constraint
    assert dsa.computation_memory(v1_node) == dsa.UNIT_SIZE * 3


def test_footprint_on_computation_object():
    v1 = Variable('v1', [0, 1, 2, 3, 4])
    v2 = Variable('v2', [0, 1, 2, 3, 4])
    c1 = relation_from_str('c1', '0 if v1 == v2 else  1', [v1, v2])
    n1 = VariableComputationNode(v1, [c1])
    n2 = VariableComputationNode(v2, [c1])
    comp_def = ComputationDef(
        n1, AlgorithmDef.build_with_default_param('dsa', mode='min'))
    c = DsaComputation(comp_def)

    # Must fix unit size otherwise the tests fails when we change the default
    # value
    dsa.UNIT_SIZE = 1

    footprint = c.footprint()
    assert footprint == 1


def test_build_computation_default_params():
    v1 = Variable('v1', [0, 1, 2, 3, 4])
    n1 = VariableComputationNode(v1, [])
    comp_def = ComputationDef(
        n1, AlgorithmDef.build_with_default_param('dsa'))
    c = DsaComputation(comp_def)
    assert c.mode == 'min'
    assert c.variant == 'B'
    assert c.stop_cycle == 0
    assert c.probability == 0.7


def test_build_computation_max_mode():
    v1 = Variable('v1', [0, 1, 2, 3, 4])
    n1 = VariableComputationNode(v1, [])
    comp_def = ComputationDef(
        n1, AlgorithmDef.build_with_default_param('dsa', mode='max'))
    c = DsaComputation(comp_def)
    assert c.mode == 'max'


def test_build_computation_with_params():
    v1 = Variable('v1', [0, 1, 2, 3, 4])
    n1 = VariableComputationNode(v1, [])
    comp_def = ComputationDef(
        n1, AlgorithmDef.build_with_default_param(
            'dsa', mode='max', params={'variant': 'C', 'stop_cycle': 10,
                                       'probability': 0.5}))
    c = DsaComputation(comp_def)
    assert c.mode == 'max'
    assert c.variant == 'C'
    assert c.stop_cycle == 10
    assert c.probability == 0.5


def test_1_unary_constraint_means_no_neighbors():
    variable = Variable('a', [0, 1, 2, 3, 4])
    c1 = UnaryFunctionRelation('c1', variable, lambda x: abs(x - 2))

    node = VariableComputationNode(variable, [c1])
    comp_def = ComputationDef(node,
                              AlgorithmDef.build_with_default_param('dsa'))

    computation = DsaComputation(comp_def=comp_def)
    assert len(computation.neighbors) == 0


def test_2_unary_constraint_means_no_neighbors():
    variable = Variable('a', [0, 1, 2, 3, 4])
    c1 = UnaryFunctionRelation('c1', variable, lambda x: abs(x - 3))
    c2 = UnaryFunctionRelation('c1', variable, lambda x: abs(x - 1) * 2)

    node = VariableComputationNode(variable, [c1, c2])
    comp_def = ComputationDef(node,
                              AlgorithmDef.build_with_default_param('dsa'))

    computation = DsaComputation(comp_def=comp_def)
    assert len(computation.neighbors) == 0


def test_one_binary_constraint_one_neighbors():

    v1 = Variable('v1', [0, 1, 2, 3, 4])
    v2 = Variable('v2', [0, 1, 2, 3, 4])

    @AsNAryFunctionRelation(v1, v2)
    def c1(v1_, v2_):
        return abs(v1_ - v2_)

    node = VariableComputationNode(v1, [c1])
    comp_def = ComputationDef(node,
                              AlgorithmDef.build_with_default_param('dsa'))

    computation = DsaComputation(comp_def=comp_def)
    assert len(computation.neighbors) == 1


def test_2_binary_constraint_one_neighbors():
    v1 = Variable('v1', [0, 1, 2, 3, 4])
    v2 = Variable('v2', [0, 1, 2, 3, 4])

    @AsNAryFunctionRelation(v1, v2)
    def c1(v1_, v2_):
        return abs(v1_ - v2_)

    @AsNAryFunctionRelation(v1, v2)
    def c2(v1_, v2_):
        return abs(v1_ + v2_)

    node = VariableComputationNode(v1, [c1, c2])
    comp_def = ComputationDef(node,
                              AlgorithmDef.build_with_default_param('dsa'))

    computation = DsaComputation(comp_def=comp_def)
    assert len(computation.neighbors) == 1


def test_3ary_constraint_2_neighbors():
    v1 = Variable('v1', [0, 1, 2, 3, 4])
    v2 = Variable('v2', [0, 1, 2, 3, 4])
    v3 = Variable('v3', [0, 1, 2, 3, 4])

    @AsNAryFunctionRelation(v1, v2, v3)
    def c1(v1_, v2_, v3_):
        return abs(v1_ - v2_ + v3_)

    node = VariableComputationNode(v1, [c1])
    comp_def = ComputationDef(node,
                              AlgorithmDef.build_with_default_param('dsa'))

    computation = DsaComputation(comp_def=comp_def)
    assert len(computation.neighbors) == 2

################################################################################


def test_select_and_send_random_value_when_starting():
    # When starting, a DSA computation select a random value and send it to
    # all neighbors
    v1 = Variable('v1', [0, 1, 2, 3, 4])
    v2 = Variable('v2', [0, 1, 2, 3, 4])
    v3 = Variable('v3', [0, 1, 2, 3, 4])

    @AsNAryFunctionRelation(v1, v2, v3)
    def c1(v1_, v2_, v3_):
        return abs(v1_ - v2_ + v3_)

    node = VariableComputationNode(v1, [c1])
    comp_def = ComputationDef(node,
                              AlgorithmDef.build_with_default_param('dsa'))

    computation = DsaComputation(comp_def=comp_def)
    message_sender = MagicMock()
    computation.message_sender = message_sender

    computation.start()

    assert computation.current_value in v1.domain
    expected_message = DsaMessage(computation.current_value)
    print("message_sender.mock_calls", message_sender.mock_calls)
    message_sender.assert_has_calls(
        [call('v1', 'v2', expected_message, None, None),
         call('v1', 'v3', expected_message, None, None)],
        any_order=True
    )

################################################################################


def test_str_dsa_class():
    variable = Variable('a', [0, 1, 2, 3, 4])
    c1 = UnaryFunctionRelation('c1', variable, lambda x: abs(x - 2))

    computation = DsaComputation(
        ComputationDef(VariableComputationNode(variable, [c1]),
                       AlgorithmDef.build_with_default_param('dsa')))

    assert str(computation) == "dsa.DsaComputation(a)"


def test_repr_dsa_class():
    variable = Variable('a', [0, 1, 2, 3, 4])
    c1 = UnaryFunctionRelation('c1', variable, lambda x: abs(x - 2))

    computation = DsaComputation(
        ComputationDef(VariableComputationNode(variable, [c1]),
                       AlgorithmDef.build_with_default_param('dsa')))

    assert repr(computation) == "dsa.DsaComputation(a)"
