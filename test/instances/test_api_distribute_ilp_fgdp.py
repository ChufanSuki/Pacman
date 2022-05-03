
"""Api tests for ILP_FGPD distribution method.
"""
from pacman.dcop.dcop import DCOP
from pacman.dcop.objects import Domain, create_variables, create_agents
from test.instances.instance import dcop_graphcoloring_3


def create_dcop():
    dcop = DCOP('test')
    # Domain and vraibales
    d = Domain('color', '', ['R', 'G'])
    variables = create_variables('v', [1, 2, 3], d)
    # unary constraints for preferences
    dcop += 'cost_1', '-0.1 if v1 == "R" else 0.1 ', variables
    dcop += 'cost_2', '-0.1 if v2 == "G" else 0.1 ', variables
    dcop += 'cost_3', '-0.1 if v3 == "G" else 0.1 ', variables
    # coloring constraints : v1 != v2 != v3
    dcop += 'c1', '1 if v1 == v2 else 0', variables
    dcop += 'c2', '1 if v3 == v2 else 0', variables

    return dcop


def test_api_distribute_maxsum_ilp_fgdp():
    from pacman.computations_graph import factor_graph
    from pacman.distribution import ilp_fgdp
    from pacman.algorithms import amaxsum

    dcop = dcop_graphcoloring_3()
    agents = create_agents('a', range(1, 4), capacity=100)
    dcop._agents_def = agents

    cg = factor_graph.build_computation_graph(dcop)
    dist = ilp_fgdp.distribute(cg, dcop.agents.values(),
                               computation_memory=amaxsum.computation_memory,
                               communication_load=amaxsum.communication_load)

    assert dist.is_hosted(['v1', 'v2', 'v3'])


def test_api_distribute_dsa_ilp_fgdp():
    from pacman.computations_graph import factor_graph
    from pacman.distribution import ilp_fgdp
    from pacman.algorithms import dsa

    dcop = dcop_graphcoloring_3()
    agents = create_agents('a', range(1, 4), capacity=100)
    dcop._agents_def = agents

    cg = factor_graph.build_computation_graph(dcop)
    dist = ilp_fgdp.distribute(cg, dcop.agents.values(),
                               computation_memory=dsa.computation_memory,
                               communication_load=dsa.communication_load)

    assert dist.is_hosted(['v1', 'v2', 'v3'])
