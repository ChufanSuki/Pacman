from typing import Sized, Iterable, Any, Union, Tuple, Dict

from pacman.utils.simple_repr import SimpleRepr

VariableName = str


class Domain(Sized, SimpleRepr, Iterable[Any]):
    """
    A VariableDomain indicates which are the valid values for variables with
    this domain. It also indicates the type of environment state represented
    by there variable : 'luminosity', humidity', etc.

    A domain object can be used like a list of value as it support basic
    list-like operations : 'in', 'len', iterable...

    >>> domain = Domain("binary", "binary", [0, 1])
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
        return "VariableDomain({})".format(self.name)

    def __repr__(self):
        return "VariableDomain({}, {}, {})".format(self.name, self.type, self.values)

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

        Examples
        --------

        >>> d = Domain('d', 'd', [1, 2, 3])
        >>> d.index(2)
        1

        """
        raise NotImplementedError()

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
        raise NotImplementedError()

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
    def __init__(self, name: str, domain: Union[Domain, Iterable[Any]], initial_value=None):
        self._name = name
        # Sanity Check for domain and initial_value
        self._domain = domain
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
        return "Variable({})".format(self.name)

    def __repr__(self):
        return "Variable({}, {}, {})".format(self.name, self.domain, self.initial_value)

    def __hash__(self):
        return hash((self.name, self.domain, self.initial_value))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Variable):
            return False
        if self.name == o.name and self.domain == o.domain and self.initial_value == o.initial_value:
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
        If it not a tuple, a variable is be created for each of
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
    raise NotImplementedError()


