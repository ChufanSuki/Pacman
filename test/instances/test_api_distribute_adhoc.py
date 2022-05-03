
"""Api tests for adhoc distribution method.
"""
from pacman.dcop.objects import create_agents
from test.instances.instance import dcop_graphcoloring_3


def test_api_distribute_maxsum_adhoc():
    from pacman.computations_graph import factor_graph
    from pacman.distribution import adhoc
    from pacman.algorithms import amaxsum

    dcop = dcop_graphcoloring_3()
    agents = create_agents('a', [1, 2, 3], capacity=100)
    dcop._agents_def = agents

    cg = factor_graph.build_computation_graph(dcop)
    dist = adhoc.distribute(cg, dcop.agents.values(),
                            computation_memory=amaxsum.computation_memory,
                            communication_load=amaxsum.communication_load)

    assert dist.is_hosted(['v1', 'v2', 'v3'])


def test_api_distribute_dsa_adhoc():
    from pacman.computations_graph import factor_graph
    from pacman.distribution import adhoc
    from pacman.algorithms import dsa

    dcop = dcop_graphcoloring_3()
    agents = create_agents('a', [1, 2, 3], capacity=100)
    dcop._agents_def = agents

    cg = factor_graph.build_computation_graph(dcop)
    dist = adhoc.distribute(cg, dcop.agents.values(),
                            computation_memory=dsa.computation_memory,
                            communication_load=dsa.communication_load)

    assert dist.is_hosted(['v1', 'v2', 'v3'])

