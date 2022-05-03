

import pytest

from pacman.computations_graph.objects import ComputationNode, Link
from pacman.utils.simple_repr import from_repr, simple_repr


def test_node_creation_minimal():
    # name is the only mandatory param:
    n = ComputationNode('n1')
    assert n.name == 'n1'
    assert not n.type
    assert not n.links
    assert not n.neighbors

def test_node_creation_with_links():

    n1 = ComputationNode('n1', links=[Link(['n2'])])

    assert 'n2' in n1.neighbors
    assert list(n1.links)[0].has_node('n2')

def test_node_creation_with_hyperlinks():

    n1 = ComputationNode('n1', links=[Link(['n2', 'n3']),
                                      Link(['n4'])])

    assert 'n2' in n1.neighbors
    assert 'n3' in n1.neighbors
    assert 'n4' in n1.neighbors

def test_node_creation_with_one_neighbor():

    n1 = ComputationNode('n1', neighbors=['n2'])

    assert 'n2' in n1.neighbors
    assert len(n1.links) == 1
    assert list(n1.links)[0].has_node('n2')

def test_node_creation_with_several_neighbors():

    n1 = ComputationNode('n1', neighbors=['n2', 'n3', 'n4'])

    assert 'n2' in n1.neighbors
    assert 'n3' in n1.neighbors
    assert 'n4' in n1.neighbors
    assert len(n1.links) == 3


def test_node_creation_raises_when_giving_links_neighbors():

    with pytest.raises(ValueError):
        n1 = ComputationNode('n1', links=[Link(['n2'])], neighbors=['n2'])


def test_node_simplerepr():
    n1 = ComputationNode('n1', neighbors=['n2', 'n3', 'n4'])

    r1 = simple_repr(n1)

    obtained = from_repr(r1)

    assert n1 == obtained
    assert 'n2' in n1.neighbors
    assert 'n3' in n1.neighbors
    assert 'n4' in n1.neighbors
    assert len(n1.links) == 3