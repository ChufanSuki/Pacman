
import unittest

from pacman.computations_graph.factor_graph import ComputationsFactorGraph, \
    VariableComputationNode, FactorComputationNode, FactorGraphLink
from pacman.computations_graph.factor_graph import build_computation_graph
from pacman.dcop.objects import Variable, Domain
from pacman.dcop.dcop import DCOP
from pacman.dcop.relations import constraint_from_str
from pacman.utils.simple_repr import simple_repr, from_repr


def test_one_var_one_factor():
    dcop = DCOP('test', 'min')
    d1 = Domain('d1', '--', [1, 2, 3])
    v1 = Variable('v1', d1)
    dcop += 'c1', '0.5 * v1', [v1]

    g = build_computation_graph(dcop)

    assert len(g.links) == 1
    assert len(g.nodes) == 2


def test_two_var_one_factor():
    dcop = DCOP('test', 'min')
    d1 = Domain('d1', '--', [1, 2, 3])
    v1 = Variable('v1', d1)
    v2 = Variable('v2', d1)
    dcop += 'c1', '0.5 * v1 + v2', [v1, v2]

    g = build_computation_graph(dcop)

    assert len(g.links) == 2
    assert len(g.nodes) == 3


def test_density_two_var_one_factor():
    dcop = DCOP('test', 'min')
    d1 = Domain('d1', '--', [1, 2, 3])
    v1 = Variable('v1', d1)
    v2 = Variable('v2', d1)
    dcop += 'c1', '0.5 * v1 + v2', [v1, v2]

    g = build_computation_graph(dcop)

    assert g.density() == 4/6


class TestFactorGraphComputation(unittest.TestCase):

    # Test computation & nodes

    def test_create_ok(self):
        d1 = Domain('d1', '', [1, 2, 3, 5])
        v1 = Variable('v1', d1)
        f1 = constraint_from_str('f1', 'v1 * 0.5', [v1])

        cv1 = VariableComputationNode(v1, [f1])
        cf1 = FactorComputationNode(f1)
        cg = ComputationsFactorGraph([cv1], [cf1])

    def test_raise_when_duplicate_computation_name(self):
        d1 = Domain('d1', '', [1, 2, 3, 5])
        v1 = Variable('v1', d1)
        # here we create a relation with the same name as the variable
        f1 = constraint_from_str('v1', 'v1 * 0.5', [v1])

        cv1 = VariableComputationNode(v1, ['f1'])
        cf1 = FactorComputationNode(f1)
        self.assertRaises(KeyError, ComputationsFactorGraph, [cv1],
                          [cf1])



def test_factornode_simple_repr():
    d1 = Domain('d1', '', [1, 2, 3, 5])
    v1 = Variable('v1', d1)
    f1 = constraint_from_str('f1', 'v1 * 0.5', [v1])

    cv1 = VariableComputationNode(v1, ['f1'])
    cf1 = FactorComputationNode(f1, )

    r= simple_repr(cf1)
    obtained = from_repr(r)

    assert obtained == cf1
    assert cf1.factor == obtained.factor


def test_variablenode_simple_repr():
    d1 = Domain('d1', '', [1, 2, 3, 5])
    v1 = Variable('v1', d1)
    f1 = constraint_from_str('f1', 'v1 * 0.5', [v1])

    cv1 = VariableComputationNode(v1, ['f1'])
    cf1 = FactorComputationNode(f1, )

    r= simple_repr(cv1)
    obtained = from_repr(r)

    assert obtained == cv1
    assert cv1.variable == obtained.variable


