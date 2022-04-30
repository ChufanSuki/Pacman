import unittest
from collections import namedtuple

from pacman.utils.graphs import as_bipartite_graph, Node, \
    find_furthest_node, \
    calc_diameter, as_networkx_graph, all_pairs, cycles_count, graph_diameter
from pacman.dcop.objects import Variable
from pacman.dcop.relations import UnaryFunctionRelation, \
    NAryFunctionRelation

import pytest


class TestAsGraph:

    def test_1var_1rel(self):
        domain = list(range(10))
        l1 = Variable('l1', domain)
        rel_l1 = UnaryFunctionRelation('rel_l1', l1, lambda x: x)

        nodes = as_bipartite_graph([l1], [rel_l1])

        assert len(nodes) == 2
        var_nodes = [n for n in nodes if n.type == 'VARIABLE']
        rel_nodes = [n for n in nodes if n.type == 'CONSTRAINT']

        assert len(var_nodes) == 1
        assert len(rel_nodes) == 1

    def test_3var_1rel(self):
        domain = list(range(10))
        l1 = Variable('l1', domain)
        l2 = Variable('l2', domain)
        l3 = Variable('l3', domain)
        rel = NAryFunctionRelation(lambda x, y, z: 0, [l1, l2, l3], name='rel')

        nodes = as_bipartite_graph([l1, l2, l3], [rel])

        assert len(nodes) == 4
        var_nodes = [n for n in nodes if n.type == 'VARIABLE']
        rel_nodes = [n for n in nodes if n.type == 'CONSTRAINT']

        assert len(var_nodes) == 3
        assert len(rel_nodes) == 1

        assert len(rel_nodes[0].neighbors), 3
        assert var_nodes[0] in rel_nodes[0].neighbors
        assert var_nodes[1] in rel_nodes[0].neighbors
        assert var_nodes[2] in rel_nodes[0].neighbors


@pytest.fixture()
def nodes():
    Content = namedtuple('Content', ['name'])
    n1 = Node(Content('n1'))
    n2 = Node(Content('n2'))
    n3 = Node(Content('n3'))
    n4 = Node(Content('n4'))
    n5 = Node(Content('n5'))

    n1.add_neighbors(n2)
    n1.add_neighbors(n3)
    n2.add_neighbors(n4)
    n3.add_neighbors(n4)
    n3.add_neighbors(n5)

    nodes = [n1, n2, n3, n4, n5]
    return nodes


class TestFindFurthestInLoopyGraph:
    # https://stackoverflow.com/questions/50132703/pytest-fixture-for-a-class-through-self-not-as-method-argument
    @pytest.fixture(autouse=True)
    def _setup_nodes(self, nodes):
        self._nodes = nodes

    def test_from_n1(self):
        furthest, distance = find_furthest_node(self._nodes[0], self._nodes)
        assert furthest == self._nodes[3] or furthest == self._nodes[4]
        assert distance == 2

    def test_from_n2(self):
        furthest, distance = find_furthest_node(self._nodes[1], self._nodes)
        assert furthest == self._nodes[4]
        assert distance == 3

    def test_from_n3(self):
        furthest, distance = find_furthest_node(self._nodes[2], self._nodes)
        assert furthest == self._nodes[1]
        assert distance == 2

    def test_from_n4(self):
        furthest, distance = find_furthest_node(self._nodes[3], self._nodes)
        assert furthest == self._nodes[4] or furthest == self._nodes[0]
        assert distance == 2

    def test_from_n5(self):
        furthest, distance = find_furthest_node(self._nodes[4], self._nodes)
        assert furthest == self._nodes[1]
        assert distance == 3


class TestGraphDiameter:

    def test_furthest_node(self):
        Content = namedtuple('Content', ['name'])
        n1 = Node(Content('n1'))
        n2 = Node(Content('n2'))
        n3 = Node(Content('n3'))
        n4 = Node(Content('n4'))

        n1.add_neighbors(n2)
        n2.add_neighbors(n3)
        n2.add_neighbors(n4)

        _, d = find_furthest_node(n1, [n1, n2, n3, n4])
        assert d == 2

        _, d = find_furthest_node(n2, [n1, n2, n3, n4])
        assert d == 1

    def test_diameter(self):
        Content = namedtuple('Content', ['name'])
        n1 = Node(Content('n1'))
        n2 = Node(Content('n2'))
        n3 = Node(Content('n3'))
        n4 = Node(Content('n4'))

        n1.add_neighbors(n2)
        n2.add_neighbors(n3)
        n2.add_neighbors(n4)

        nodes = [n1, n2, n3, n4]

        assert calc_diameter(nodes) == 2

    def test_diameter_5nodes(self):
        Content = namedtuple('Content', ['name'])
        n1 = Node(Content('n1'))
        n2 = Node(Content('n2'))
        n3 = Node(Content('n3'))
        n4 = Node(Content('n4'))
        n5 = Node(Content('n5'))
        n6 = Node(Content('n6'))

        n1.add_neighbors(n2)
        n2.add_neighbors(n3)
        n2.add_neighbors(n4)
        n4.add_neighbors(n5)
        n5.add_neighbors(n6)

        nodes = [n1, n2, n3, n4, n5, n6]

        assert calc_diameter(nodes) == 4

    def test_diameter_loop(self):
        Content = namedtuple('Content', ['name'])
        n1 = Node(Content('n1'))
        n2 = Node(Content('n2'))
        n3 = Node(Content('n3'))
        n4 = Node(Content('n4'))
        n5 = Node(Content('n5'))

        n1.add_neighbors(n2)
        n1.add_neighbors(n3)
        n2.add_neighbors(n4)
        n3.add_neighbors(n4)
        n3.add_neighbors(n5)

        nodes = [n1, n2, n3, n4, n5]

        # FIXME: cycles count only works on trees !!
        # self.assertEqual(calc_diameter(nodes), 3)


class TestNetworkX:

    def test_pairs_2elt(self):
        elts = ['a', 'b']
        pairs = all_pairs(elts)
        assert len(pairs) == 1
        assert pairs[0] == ('a', 'b')

    def test_pairs_3elt(self):
        elts = ['a', 'b', 'c']
        pairs = all_pairs(elts)
        assert len(pairs) == 3
        assert ('a', 'b') in pairs
        assert ('a', 'c') in pairs
        assert ('b', 'c') in pairs

    def test_pairs_delt(self):
        elts = ['a', 'b', 'c', 'd']
        pairs = all_pairs(elts)
        assert len(pairs) == 6
        assert ('a', 'b') in pairs
        assert ('a', 'c') in pairs
        assert ('a', 'd') in pairs
        assert ('b', 'c') in pairs
        assert ('b', 'd') in pairs
        assert ('c', 'd') in pairs

    def test_convert_graph_simple(self):
        domain = list(range(10))
        l1 = Variable('l1', domain)
        l2 = Variable('l2', domain)
        l3 = Variable('l3', domain)
        r1 = NAryFunctionRelation(lambda x, y: 0, [l1, l2], name='r1')
        r2 = NAryFunctionRelation(lambda x, y: 0, [l2, l3], name='r2')
        r3 = NAryFunctionRelation(lambda x, y: 0, [l1, l3], name='r3')

        graph = as_networkx_graph([l1, l2, l3], [r1, r2, r3])

        print(graph.edges())
        print(graph.nodes())

        assert len(graph.nodes()) == 3
        assert len(graph.edges()) == 3

    def test_convert_graph(self):
        domain = list(range(10))
        l1 = Variable('l1', domain)
        l2 = Variable('l2', domain)
        l3 = Variable('l3', domain)
        l4 = Variable('l4', domain)

        # 4-ary relation : iot defines a clique with l1, l2, l3, l4
        r1 = NAryFunctionRelation(lambda x, y: 0, [l1, l2, l3, l4], name='r1')

        graph = as_networkx_graph([l1, l2, l3], [r1])

        print(graph.edges())
        print(graph.nodes())

        assert len(graph.nodes()) == 4
        assert len(graph.edges()) == 6


    def test_count_cycle_none(self):
        domain = list(range(10))

        l1 = Variable('l1', domain)
        l2 = Variable('l2', domain)
        l3 = Variable('l3', domain)
        r1 = NAryFunctionRelation(lambda x, y: 0, [l1, l2], name='r1')
        r2 = NAryFunctionRelation(lambda x, y: 0, [l2, l3], name='r2')

        n = cycles_count([l1, l2, l3], [r1, r2])

        assert n == 0

    def test_count_cycle_one(self):
        domain = list(range(10))

        l1 = Variable('l1', domain)
        l2 = Variable('l2', domain)
        l3 = Variable('l3', domain)
        r1 = NAryFunctionRelation(lambda x, y: 0, [l1, l2], name='r1')
        r2 = NAryFunctionRelation(lambda x, y: 0, [l2, l3], name='r2')
        r3 = NAryFunctionRelation(lambda x, y: 0, [l1, l3], name='r3')

        n = cycles_count([l1, l2, l3], [r1, r2, r3])

        assert n == 1

    def test_count_cycle_clique(self):
        domain = list(range(10))

        l1 = Variable('l1', domain)
        l2 = Variable('l2', domain)
        l3 = Variable('l3', domain)
        l4 = Variable('l4', domain)
        r1 = NAryFunctionRelation(lambda x, y, z, w: 0, [l1, l2, l3, l4],
                                  name='r1')

        n = cycles_count([l1, l2, l3, l4], [r1])

        assert n == 3

    def test_diameter_simple(self):
        l1 = Variable('l1', [])
        l2 = Variable('l2', [])
        l3 = Variable('l3', [])
        r1 = NAryFunctionRelation(lambda x, y: 0, [l1, l2], name='r1')
        r2 = NAryFunctionRelation(lambda x, y: 0, [l2, l3], name='r2')

        d = graph_diameter([l1, l2, l3], [r1, r2])
        assert len(d) == 1
        assert d[0] == 2

    def test_diameter_simple2(self):
        l1 = Variable('l1', [])
        l2 = Variable('l2', [])
        l3 = Variable('l3', [])
        r1 = NAryFunctionRelation(lambda x, y: 0, [l1, l2], name='r1')
        r2 = NAryFunctionRelation(lambda x, y: 0, [l2, l3], name='r2')
        r3 = NAryFunctionRelation(lambda x, y: 0, [l1, l3], name='r3')

        d = graph_diameter([l1, l2, l3], [r1, r2, r3])
        assert d == [1]

    def test_diameter_simple3(self):
        l1 = Variable('l1', [])
        l2 = Variable('l2', [])
        l3 = Variable('l3', [])
        r1 = NAryFunctionRelation(lambda x, y: 0, [l1, l2], name='r1')

        g = as_networkx_graph([l1, l2, l3], [r1])

        d = graph_diameter([l1, l2, l3], [r1])
        assert sorted(d) == [0, 1]
