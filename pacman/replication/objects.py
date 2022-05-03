

from typing import Dict, List

from collections import defaultdict

from pacman.algorithms import ComputationDef
from pacman.infrastructure.computations import Message


class ReplicaDistribution(object):
    """
    Simply a convenient representation of the distribution of replica on agents

    """

    def __init__(self, mapping: Dict[str, List[str]]):
        """
        Basic
        :param mapping: map computation -> list of agents hosting a replica
        for this computation.
        """
        self._mapping = mapping  # type: Dict[str, List[str]]
        self._agent_replicas = \
            defaultdict(lambda: [])  # type: Dict[str, List[str]]

        for c in self._mapping:
            for a in self._mapping[a]:

                if c in self._agent_replicas[a]:
                    raise ValueError('Agent {} is hosting several replica '
                                     'for {}'.format(a, c))
                self._agent_replicas[a].append(c)

    def replicas_on(self, agt: str, raise_on_unknown=False):
        try:
            return list(self._agent_replicas[agt])
        except KeyError as ke:
            if raise_on_unknown:
                raise ke
            return []

    def agents_for_computation(self, computation: str):
        return list(self._mapping[computation])
