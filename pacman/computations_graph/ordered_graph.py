
from typing import Iterable, Optional

from pacman.computations_graph.objects import ComputationNode, ComputationGraph, Link
from pacman.dcop.dcop import DCOP
from pacman.dcop.objects import Variable
from pacman.dcop.relations import Constraint, find_dependent_relations
from pacman.utils.simple_repr import from_repr, simple_repr


class VariableComputationNode(ComputationNode):
    def __init__(
        self, variable: Variable, constraints: Iterable[Constraint], name: str = None
    ) -> None:
        if name is None:
            name = variable.name
        links = []
        for c in constraints:
            links.append(
                ConstraintLink(name=c.name, nodes=[v.name for v in c.dimensions])
            )
        super().__init__(name, "VariableComputationNode", links=links)
        self._variable = variable
        self._constraints = constraints

    @property
    def variable(self):
        return self._variable

    @property
    def constraints(self):
        return self._constraints

    def get_previous(self):
        for l in self.links:
            if l.type == "previous":
                return l.target
        return None

    def get_next(self):
        for l in self.links:
            if l.type == "next":
                return l.target
        return None

    def __eq__(self, other):
        if type(other) != VariableComputationNode:
            return False
        if self.variable == other.variable and self.constraints == other.constraints:
            return True
        return False

    def __str__(self):
        return "VariableComputationNode({})".format(self._variable.name)

    def __repr__(self):
        return "VariableComputationNode({}, {})".format(
            self._variable, self.constraints
        )

    def __hash__(self):
        return hash(
            (self._name, self._node_type, self.variable, tuple(self.constraints))
        )


class ConstraintLink(Link):
    def __init__(self, name: str, nodes: Iterable[str]) -> None:
        super().__init__(nodes, link_type="constraint_link")
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self):
        return "ConstraintLink({})".format(self._name)

    def __repr__(self):
        return "ConstraintLink({}, {})".format(self._name, self.nodes)

    def __eq__(self, other):
        if super().__eq__(other) and self.name == other.name:
            return True
        return False

    def __hash__(self):
        return hash((self.type, self.nodes))


class OrderLink(Link):
    def __init__(self, link_type: str, link_source: str, link_target) -> None:
        super().__init__(link_type=link_type, nodes=[link_source, link_target])
        if link_type not in ["previous", "next"]:
            raise ValueError(
                f"Invalid link type in OrderedGraph : {link_type} "
                f"between {link_source} and {link_target}"
                f"Supported types are 'previous','next'"
            )
        self._source = link_source
        self._target = link_target

    @property
    def source(self) -> str:
        """ The source of the link.

        Returns
        -------
        str
            The name of source PseudoTreeNode computation node.
        """
        return self._source

    @property
    def target(self):
        """ The target of the link.

        Returns
        -------
        str
            The name of target PseudoTreeNode computation node.
        """
        return self._target

    def _simple_repr(self):
        r = {
            "__module__": self.__module__,
            "__qualname__": self.__class__.__qualname__,
            "type": self.type,
            "source": simple_repr(self.source),
            "target": simple_repr(self.target),
        }
        return r

    @classmethod
    def _from_repr(cls, r):
        return OrderLink(r["type"], from_repr(r["source"]), from_repr(r["target"]))


class OrderedConstraintGraph(ComputationGraph):
    def __init__(self, nodes: Iterable[VariableComputationNode]) -> None:
        super().__init__(nodes=nodes, graph_type="ConstraintHyperGraph")

        # Add order links
        sorted_nodes = sorted(self.nodes, key=lambda n: n.name)

        for n1, n2 in zip(sorted_nodes[:-1], sorted_nodes[1:]):
            # n1 next is n2
            n1.links.append(OrderLink("next", n1.name, n2.name))
            # n2 prev is n1
            n2.links.append(OrderLink("previous", n2.name, n1.name))


def build_computation_graph(
    dcop: Optional[DCOP] = None,
    variables: Iterable[Variable] = None,
    constraints: Iterable[Constraint] = None,
) -> OrderedConstraintGraph:
    computations = []
    if dcop is not None:
        if constraints or variables is not None:
            raise ValueError(
                "Cannot use both dcop and constraints / " "variables parameters"
            )
        for v in dcop.variables.values():
            var_constraints = find_dependent_relations(v, dcop.constraints.values())
            computations.append(VariableComputationNode(v, var_constraints))
    else:
        if constraints is None or variables is None:
            raise ValueError(
                "Constraints AND variables parameters must be "
                "provided when not building the graph from a dcop"
            )
        for v in variables:
            var_constraints = find_dependent_relations(v, constraints)
            computations.append(VariableComputationNode(v, var_constraints))

    return OrderedConstraintGraph(computations)
