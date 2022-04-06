class DCOP:
    r"""A DCOP representation.

    A DCOP is a Constraints Optimization Problem distribution on a set of
    agents: agents send messages to each other to find a solution to the
    optimization problem.
    A DCOP is traditionally represented as a tuple .. math:: (V, D, C, A, \mu) where A
    is a set of variables, D the set of the domain for these variables, C a set
    of constraints involving these variables, A a set of agents responsible
    for selecting the value of the variable and \mu is a mapping of the
    variable to the agents.
    Given these elements, the goal is to find an assignment of values to
    variables that minimizes the sum of the costs from the constants.

    In pyDcop, a DCOP does not contains the mapping \mu as this mapping
    depends on the algorithm used to solve the constraints optimization.

    Parameter
    ---------
    name: str
        The name of the problem
    description: str
        A description of the problem
    variables: dict of variable name, as str, to Variable
    domains: dict of domain name, as str, to Variable
    constraints: dict of constraint name, as str to Constraint
    agents: dict of agent name, as str, to Agent
    """

    def __init__(self, name, description, variables, domain, constraints, agents):
        self.name = name
        self.description = description
        self.variables = variables
        self.domain = domain
        self.constraints = constraints
        self.agents = agents
        self.__check_consistency()

    def __check_consistency(self):
        """Check consistency of the DCOP.

        Check that the number of variables, domain, constraints and agents
        are consistent.
        """
        if len(self.variables) != len(self.domain):
            raise ValueError("The number of variables and domain are not the " "same")
        if len(self.variables) != len(self.constraints):
            raise ValueError(
                "The number of variables and constraints are not " "the same"
            )
        if len(self.variables) != len(self.agents):
            raise ValueError("The number of variables and agents are not the " "same")

    def __str__(self):
        """Return a string representation of the DCOP."""
        return (
            "DCOP(name={}, description={}, variables={}, domain={}, "
            "constraints={}, agents={})".format(
                self.name,
                self.description,
                self.variables,
                self.domain,
                self.constraints,
                self.agents,
            )
        )

    def __repr__(self):
        """Return a string representation of the DCOP."""
        return (
            "DCOP(name={}, description={}, variables={}, domain={}, "
            "constraints={}, agents={})".format(
                self.name,
                self.description,
                self.variables,
                self.domain,
                self.constraints,
                self.agents,
            )
        )
