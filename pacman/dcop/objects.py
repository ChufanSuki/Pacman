import itertools
from typing import Any, Dict, Iterable, Sized, Tuple, Union

from pacman.utils.simple_repr import SimpleRepr

VariableName = str


class Domain(Sized, SimpleRepr, Iterable[Any]):
    """
    A VariableDomain indicates which are the valid values for variables with
    this domain. It also indicates the type of environment state represented
    by there variable : 'luminosity', humidity', etc.

    A domain object can be used like a list of value as it support basic
    list-like operations : 'in', 'len', iterable...

    >>> binary_domain = Domain("binary", "binary", [0, 1])
    """

    def __init__(self, name: str, domain_type: str, values: Iterable):
        """
        :param name: The name of the domain
        :param domain_type: A string indetifying the kind of value in the domaibn. For example:
        :param values: an array containing the values allowed for the
                       variables with this domain.
        """
        self._name = name
        self._domain_type = domain_type
        # we don't want to mutate the values, so a tuple is used for faster and safer code
        self._values = tuple(values)

    @property
    def type(self) -> str:
        return self._domain_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def values(self) -> Iterable:
        return self._values

    def __iter__(self):
        # returns the array
        return self._values.__iter__()

    def __getitem__(self, index):
        return self._values[index]

    def __len__(self):
        return len(self._values)

    def __contains__(self, v):
        return v in self._values

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Domain):
            return False
        if self.name == o.name and self.values == o.values and self.type == o.type:
            return True

        return False

    def __str__(self):
        return f"VariableDomain({self.name})"

    def __repr__(self):
        return f"VariableDomain({self.name}, {self.type}, {self.values})"

    def __hash__(self):
        return hash((self._name, self._domain_type, self._values))

    def index(self, val):
        """
        Find the position of a value in the domain

        Parameters
        ----------
        val:
            a value to look for in the domain

        Returns
        -------
        the index of this value in the domain.

        Error
        -----
        If the value is not in the domain, an ValueError is raised.

        Examples
        --------

        >>> d = Domain('d', 'd', [1, 2, 3])
        >>> d.index(2)
        1

        """
        for i, v in enumerate(self._values):
            if v == val:
                return i
        raise ValueError(f"{val} is not in the domain {self._name}")

    def to_str(self, val: Any) -> str:
        """
        Convert a value to a string representation

        Parameters
        ----------
        val:
            a value in the domain

        Returns
        -------
        a string representation of the value

        Examples
        --------

        >>> d = Domain('d', 'd', [1, 2, 3])
        >>> d.to_str(2)
        '2'

        """
        return str(val)

    def to_domain_value(self, val: str):
        """
        Find a domain value with the same str representation

        This is useful when reading value from a file.

        Parameters
        ----------
        val : str
            a string that should match a value in the domain (which may
            contains non-string values, eg int)

        Returns
        -------
        a pair (index, value) where index is the position of the value in the
        domain and value the actual value that matches val.

        Examples
        --------

        >>> d = Domain('d', 'd', [1, 2, 3])
        >>> d.to_domain_value('2')
        (1, 2)

        """
        for i, v in enumerate(self._values):
            if str(v) == val:
                return i, v
        raise ValueError(f"{val} is not in the domain {self._name}")


class Variable(SimpleRepr):
    """A DCOP variable.

    This class represents the definition of a variable : a name, a domain
    where the variable can take it's value and an optional initial value. It
    is not used to keep track of the current value assigned to the variable.

    Parameters
    ----------
    name: str
        Name of the variable. You must use a valid python identifier if you
        want to use python expression (given as string) to define
        constraints using this variable.
    domain: Domain or Iterable
        The domain where this variable can take its value. If an iterable
        is given a Domain object is automatically created (named after
        the variable name: `d_<var_name>`.
    initial_value: Any
        The initial value assigned to the variable.

    """

    def __init__(
        self, name: str, domain: Union[Domain, Iterable[Any]], initial_value=None
    ):
        self._name = name
        # Sanity Check for domain and initial_value
        if domain is None:
            raise ValueError("domain cannot be None")
        if isinstance(domain, Domain):  # Note that Domain is also Iterable
            self._domain = domain
        elif isinstance(domain, Iterable):
            domain = Domain(f"d_{name}", "unknown", domain)
            self._domain = domain
        else:
            raise TypeError("domain is not Domain or Iterable")
        if initial_value is not None:
            if initial_value not in self._domain:
                raise ValueError(f"initial value {initial_value} is not in the domain")
        self._initial_value = initial_value

    @property
    def name(self) -> str:
        return self._name

    @property
    def domain(self) -> Domain:
        return self._domain

    @property
    def initial_value(self) -> Any:
        return self._initial_value

    def __str__(self):
        return f"Variable({self.name})"

    def __repr__(self):
        return f"Variable({self.name}, {self.domain}, {self.initial_value})"

    def __hash__(self):
        return hash((self.name, self.domain, self.initial_value))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Variable):
            return False
        if (
            self.name == o.name
            and self.domain == o.domain
            and self.initial_value == o.initial_value
        ):
            return True

        return False

    def clone(self):
        return Variable(self.name, self.domain, self.initial_value)


def create_variables(
    name_prefix: str,
    indexes: Union[str, Tuple, Iterable],
    domain: Domain,
    separator: str = "_",
) -> Dict[Union[str, Tuple[str, ...]], Variable]:
    """Mass creation of variables.

    Parameters
    ----------
    name_prefix: str
        Used as prefix when naming the variables.
    indexes: non-tuple iterable of indexes or tuple of iterables of indexes
        If it not a tuple, a variable is created for each of
        the index. The index might be a range(see examples).
         If it is a tuple of iterable, a variable is created
        for every possible combinations of values from `indexes`.
    domain: Domain
        The domain for the variables.
    separator: str

    Returns
    -------
    dict
        A dictionary ( index -> variable) where index is a string or a
        tuple of string.

    See Also
    --------
    create_binary_variables

    Examples
    --------
    When passing an iterable of indexes:
    >>> vrs = create_variables('x_', ['a1', 'a2', 'a3'],
    ...                        Domain('color', '', ['R', 'G', 'B']))
    >>> assert isinstance(vrs['x_a2'], Variable)
    >>> assert 'B' in vrs['x_a3'].domain

    When passing a range:
    >>> vrs = create_variables('v', range(10),
    ...                        Domain('color', '', ['R', 'G', 'B']))
    >>> assert isinstance(vrs['v2'], Variable)
    >>> assert 'B' in vrs['v3'].domain


    When passing a tuple of iterables of indexes:
    >>> vrs = create_variables('m_',
    ...                        (['x1', 'x2'],
    ...                         ['a1', 'a2', 'a3']),
    ...                        Domain('color', '', ['R', 'G', 'B']))
    >>> assert isinstance(vrs[('x2', 'a3')], Variable)
    >>> assert vrs[('x2', 'a3')].name == 'm_x2_a3'
    >>> assert 'R' in vrs[('x2', 'a3')].domain

    """
    variables = {}
    if isinstance(indexes, tuple):
        for i in itertools.product(*indexes):
            name = name_prefix + separator.join(i)
            variables[i] = Variable(name, domain)
    elif isinstance(indexes, range):
        for i in indexes:
            name = name_prefix + str(i)
            variables[name] = Variable(name, domain)
    elif isinstance(indexes, Iterable):
        for i in indexes:
            name = name_prefix + str(i)
            variables[name] = Variable(name, domain)
    else:
        raise TypeError("indexes must be an iterable or range or tuple of iterables")
    return variables


class AgentDef(SimpleRepr):
    """Definition of an agent.

    AgentDef objects are used when only the definition of the agent is needed,
    and not the actual running agents. This is for example the case when
    computing the computations' distribution, or when instantiating concrete
    agents.

    Notes
    -----
    Route cost default to 1 because they are typically used as a multiplier
    for message cost when calculating communication cost.
    On the other hand, hosting cost default to 0 because they are used in a
    sum.
    In order to allow using problem-specific attribute on agents, any named
    argument passed when creating an AgentDef is available as an attribute

    Examples
    --------

    >>> a1 = AgentDef('a1', foo='bar')
    >>> a1.name
    'a1'
    >>> a1.foo
    'bar'


    Parameters
    ----------
    name: str
        the name of the agent
    capacity: int
        the capacity of the agent
    default_route: float
        the default cost of a route when not specified in routes.
    routes: dictionary of agents name, as string, to float
        attribute a specific route cost between this agent and the agents
        whose names are used as key in the dictionary
    default_hosting_cost: float
        the default hosting for a computation when not specified in
        hosting_costs.
    hosting_costs: dictionary of computation name, as string, to float
        attribute a specific cost for hosting the computations
        whose names are used as key in the dictionary.
    kwargs: dictionary string -> any
        any extra attribute that should be available on this AgentDef
        object.

    """

    def __init__(
        self,
        name: str,
        capacity: int = 100,
        default_route: float = 1,
        routes: dict = None,
        default_hosting_cost: float = 0,
        hosting_costs: dict = None,
        **kwargs,
    ):
        self._name = name
        self._capacity = capacity
        self._default_route = default_route
        self._routes = routes or {}
        self._default_hosting_cost = default_hosting_cost
        self._hosting_costs = hosting_costs or {}
        self.__dict__.update(kwargs)

    @property
    def name(self):
        return self._name

    @property
    def capacity(self):
        return self._capacity

    def hosting_cost(self, computation: str) -> float:
        """Return the hosting cost for a computation.

        Parameters
        ----------
        computation: str
            the name of the computation

        Returns
        -------
        float
            the hosting cost for the computation

        Examples
        --------
        >>> a1 = AgentDef('a1', foo='bar')
        >>> a1.hosting_cost('c1')
        0.0

        >>> a2 = AgentDef('a2', foo='bar', hosting_costs={'c1': 1.0})
        >>> a2.hosting_cost('c1')
        1.0

        >>> a3 = AgentDef('a3', foo='bar', default_hosting_cost=6, hosting_costs={'c1': 1.0, 'c2': 2.0})
        >>> a3.hosting_cost('c1')
        1.0
        >>> a3.hosting_cost('c2')
        2.0
        >>> a3.hosting_cost('c3')
        6.0
        """
        if computation in self._hosting_costs:
            return self._hosting_costs[computation]
        else:
            return self._default_hosting_cost

    def route(self, agent: str) -> float:
        """Return the route cost between this agent and another agent.

        Parameters
        ----------
        agent: str
            the name of the agent

        Returns
        -------
        float
            the route cost between this agent and the other agent

        Examples
        --------
        >>> a1 = AgentDef('a1', foo='bar')
        >>> a1.route('a2')
        1.0

        >>> a2 = AgentDef('a2', foo='bar', routes={'a1': 0.5})
        >>> a2.route('a1')
        0.5

        >>> a3 = AgentDef('a3', foo='bar', default_route=2, routes={'a1': 0.5, 'a2': 0.5})
        >>> a3.route('a1')
        0.5
        >>> a3.route('a2')
        0.5
        >>> a3.route('a3')
        2.0
        """
        if agent in self._routes:
            return self._routes[agent]
        else:
            return self._default_route


def create_agents(
    name_prefix: str,
    indexes: Union[Iterable, Tuple[Iterable]],
    default_route: float = 1,
    routes: Dict[str, float] = None,
    default_hosting_costs: float = 0,
    hosting_costs: Dict[str, float] = None,
    separator: str = "_",
    **kwargs: Union[str, int, float],
) -> Dict[Union[str, Tuple[str, ...]], AgentDef]:
    """Mass creation of agents definitions.

    Parameters
    ----------
    name_prefix: str
        Used as prefix when naming the agents.
    indexes: non-tuple iterable of indexes or tuple of iterable of indexes
        If it not a tuple, an AgentDef is be created for each of
        the index. If it is a tuple of iterable, an AgentDef is created
        for every possible combinations of values from `indexes`.
    default_route: float
        The default cost of a route when not specified in routes.
    routes: dictionary of agents name, as string, to float
        Attribute a specific route cost between this agent and the agents
        whose names are used as key in the dictionary
    default_hosting_costs
        The default hosting for a computation when not specified in
        hosting_costs.
    hosting_costs: dictionary of computation name, as string, to float
        Attribute a specific cost for hosting the computations
        whose names are used as key in the dictionary.
    separator: str
    kwargs: dictionary

    Returns
    -------
    dict
        A dictionary ( index -> AgentDef) where index is a string or a
        tuple of string.

    See Also
    --------
    create_variables

    Examples
    --------
    When passing an iterable of indexes:
    >>> agts = create_agents('a', ['1', '2', '3'],
    ...                      default_route=2, default_hosting_costs=7)
    >>> assert isinstance(agts['a2'], AgentDef)

    When passing a range:
    >>> agts = create_agents('a', range(20),
    ...                      default_route=2, default_hosting_costs=7)
    >>> assert isinstance(agts['a08'], AgentDef)

    When passing a tuple of iterables of indexes:
    >>> agts = create_agents('a', (['1', '2', '3'], ['x', 'y', 'z']), default_route=2, default_hosting_costs=7)
    >>> assert isinstance(agts[('1', 'z')], AgentDef)
    >>> assert isinstance(agts[('2', 'x')], AgentDef)
    >>> assert agts[('2', 'x')].name == 'a2_x'
    """
    if isinstance(indexes, tuple):
        indexes = itertools.product(*indexes)

    agts = {}
    for index in indexes:
        if isinstance(index, tuple):
            name = separator.join(index)
        else:
            name = index = name_prefix + str(index)
        agts[index] = AgentDef(
            name=name,
            default_route=default_route,
            routes=routes,
            default_hosting_cost=default_hosting_costs,
            hosting_costs=hosting_costs,
            **kwargs,
        )
    return agts
