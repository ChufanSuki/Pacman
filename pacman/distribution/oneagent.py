
"""

The ``oneagent`` distribution algorithm assigns exactly one computation to each
agent in the system.

It is the most simple distribution and, when used with many DCOP algorithms,
it replicates the traditional hypothesis used in the DCOP literature
where each agent is responsible for exactly one variable.

Note that this applies to algorithms using a computation-hyper graph model,
like DSA, MGM, etc.

The ``oneagent`` distribution does not define any notion of distribution cost.


Functions
---------

.. autofunction:: pacman.distribution.oneagent.distribute

.. autofunction:: pacman.distribution.oneagent.distribution_cost


"""

from typing import List, Dict, Iterable, Callable
from collections import defaultdict

from pacman.computations_graph.objects import ComputationGraph, ComputationNode
from pacman.dcop.objects import AgentDef
from pacman.distribution.objects import Distribution, DistributionHints, \
    ImpossibleDistributionException


def distribution_cost(distribution: Distribution,
                      computation_graph: ComputationGraph,
                      agentsdef: Iterable[AgentDef],
                      computation_memory: Callable[[ComputationNode], float],
                      communication_load: Callable[[ComputationNode, str],
                                                   float]) -> float:
    """
    As the ``oneagent`` distribution does not define any notion of
    distribution cost, this function always returns 0.

    Parameters
    ----------
    distribution
    computation_graph
    agentsdef
    computation_memory
    communication_load

    Returns
    -------
    distribution cost:
        0
    """
    return 0, 0, 0

def distribute(computation_graph: ComputationGraph,
               agentsdef: Iterable[AgentDef],
               hints: DistributionHints=None,
               computation_memory=None,
               communication_load=None,
               timeout= None)-> Distribution:
    """
    Simplistic distribution method: each computation is hosted on agent
    agent and each agent host a single computation.
    Agent capacity is not considered.

    Raises an ImpossibleDistributionException

    Parameters
    ----------
    computation_graph: a ComputationGraph
         the computation graph containing the computation that must be
         distributed
    agentsdef: iterable of AgentDef objects
        The definition of the agents the computation will be assigned to.
        There **must** be at least as many agents as computations.
    hints:
        Not used by the ``oneagent`` distribution method.
    computation_memory:
        Not used by the ``oneagent`` distribution method.
    computation_memory:
        Not used by the ``oneagent`` distribution method.

    Returns
    -------
    distribution: Distribution
        A Distribution object containing the mapping form agents to
        computations.
    """

    agents = list(agentsdef)

    if len(agents) < len(computation_graph.nodes):
        raise ImpossibleDistributionException(
            'Not enough agents for one agent for each computation : {} < {}'
                .format(len(agents),len(computation_graph.nodes)))

    agent_names = [a.name for a in agents]
    distribution = defaultdict(lambda : list())
    for n, a in zip(computation_graph.nodes, agent_names):
        distribution[a].append(n.name)

    return Distribution(distribution)