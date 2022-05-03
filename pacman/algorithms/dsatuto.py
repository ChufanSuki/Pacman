
"""

This module contains a very simple implementation of DSA, for demonstration
purpose.

To keep things as simple as possible, we implemented the bare minimum,
and avoided some details you would generally care about:

* no algorithm parameters (threshold, variants, etc.)
* no computation footprint nor message size

"""


from typing import Any, Tuple, List, Optional

from numpy import random

from pacman.algorithms import ComputationDef
from pacman.dcop.relations import assignment_cost, find_optimal
from pacman.infrastructure.computations import (
    VariableComputation,
    message_type,
    register,
    SynchronousComputationMixin,
)

# Type of computations graph that must be used with dsa
GRAPH_TYPE = "constraints_hypergraph"

DsaMessage = message_type("dsa_value", ["value"])


class DsaTutoComputation(SynchronousComputationMixin, VariableComputation):
    """
    A very simple DSA implementation.

    Parameters
    ----------
    variable: Variable
        an instance of Variable, whose this computation is responsible for
    constraints: an iterable of constraints objects
        The constraints the variables depends on
    computation_definition: ComputationDef
        the definition of the computation, given as a ComputationDef instance.

    """

    def __init__(self, computation_definition: ComputationDef):
        super().__init__(computation_definition.node.variable, computation_definition)

        assert computation_definition.algo.algo == "dsatuto"
        self.mode = computation_definition.algo.mode

        self.constraints = computation_definition.node.constraints

    def on_start(self):
        self.random_value_selection()
        self.logger.debug(f"Random value selected at startup : {self.current_value}")
        self.post_to_all_neighbors(DsaMessage(self.current_value))

    @register("dsa_value")
    def on_value_msg(self, variable_name, recv_msg, t):
        # No implementation here, simply used to declare the kind of message supported
        # by this computation
        pass

    def on_new_cycle(self, messages, cycle_id) -> Optional[List]:

        assignment = {self.variable.name: self.current_value}
        for sender, (message, t) in messages.items():
            assignment[sender] = message.value

        self.logger.debug(
            f"Full neighbors assignment for cycle {self.cycle_count} : {assignment}"
        )

        current_cost = assignment_cost(assignment, self.constraints)
        # Compute best local cost, based on current neighbors values:
        arg_min, min_cost = find_optimal(
            self.variable, assignment, self.constraints, self.mode
        )

        self.logger.debug(
            f"Evaluate cycle {self.cycle_count}: current cost {current_cost} - best cost {min_cost}"
        )

        if current_cost - min_cost > 0 and 0.5 > random.random():
            self.value_selection(arg_min[0])
            self.logger.debug(f"Select new value {arg_min} for better cost {min_cost} ")
        else:
            self.logger.debug(f"Do not change value {self.current_value}")

        self.post_to_all_neighbors(DsaMessage(self.current_value))
