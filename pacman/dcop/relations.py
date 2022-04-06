from typing import Any, Dict, List, Tuple

from pacman.dcop.objects import Variable
from pacman.utils.simple_repr import SimpleRepr


class RelationProtocol:
    """
    This class is used to define a protocol that must be implemented by any
    object that represents a Relation. It is meant to be usable with many
    algorithms, like for example dpop and maxsum.

    It is mostly defined for documentation purpose, objects used for are not
    required to inherit from this class as long as they implement the methods
    defined here.

    Relation objects MUST be immutable and impletemnt `__eq__()` and
    `__hash__()`. This means that methods like  `set_value_for_assignment`
    must return a new relation instead of modifying the current one.
    """

    @property
    def name(self) -> str:
        raise NotImplementedError("name not implemented")

    @property
    def dimensions(self) -> List[Variable]:
        """
        The dimensions of a relation is the list of variables it depends on.
        Returns: a list of Variable objects
        """
        raise NotImplementedError("dimensions not implemented")

    @property
    def scope_names(self) -> List[str]:
        """
        Returns: a list of variable names in the scope of the relation
        """
        return [variable.name for variable in self.dimensions]

    @property
    def arity(self) -> int:
        """
        Returns: the number of variables in the scope of the relation
        """
        return len(self.dimensions)

    @property
    def shape(self) -> Tuple[int, ...]:
        """
        The shape of a relation is defined as a tuple containing the size of the domain of each variable in dimensions.
        Returns: the shape of the relation
        """
        return tuple(len(variable.domain) for variable in self.dimensions)

    def slice(self, partial_assignment: Dict[str, object]) -> "RelationProtocol":
        """
        Slice operation on a relation.
        Parameters:
            partial_assignment: a dictionary of variable name, as string, to value
        Returns: a new relation with the variables in partial_assignment set to the given value
        """
        raise NotImplementedError("slice not implemented")

    def set_value_for_assignment(
        self, assignment: Dict[str, Any], relation_value
    ) -> "RelationProtocol":
        """

        Return a new relation with the same name and the same value for
        every possible assignment except `assignment`, which maps to
        `relation_value`.

        This method is optional: many concrete Relation implements will
        probably not implement it. In that case they should raise an
        `NotImplemented` exception.

        :param assignment: a full assignment for the relation, containing one
        value for each of the variable this relation depends on.
        :param relation_value: the value of the relation for this assignment.

        :return a new Relation object
        """
        raise NotImplementedError("set_value_for_assignment not implemented")

    def get_value_for_assignment(self, assignment: List[Any]) -> Any:
        """
        Get constraint value for an assignment.

        Notes
        -----
        Relying on dimension order (i.e. passing the assignment as a list)
        is fragile and discouraged, use dict or keyword arguments whenever
        possible instead !


        Parameters
        ----------
        assignment: a list of value
            a full assignment for the relation, containing one
            value for each of the variable this relation depends on. It must be
            either a list of values, in the same order as the dimensions of the
            relation, or a dict { var_name: value}

        Returns
        -------
        the value of the relation for this assignment.
        """
        raise NotImplementedError("get_value_for_assignment not implemented")


class AbstractBaseRelation(RelationProtocol):
    """
    This class is meant to be used as a base when implementing a Relation.
    """

    def __init__(self, name: str) -> None:
        self._name = name
        self._variables = []  # type: List[Variable]

    @property
    def name(self) -> str:
        return self._name

    @property
    def dimensions(self) -> List[Variable]:
        return self._variables

    def __str__(self):
        return f"Relation: {self._name}  on {self._variables} "


class ZeroAryityRelation(AbstractBaseRelation, SimpleRepr):
    def __init__(self, name: str, value: Any) -> None:
        super().__init__(name)
        self._value = value
        self._variables = []

    def __str__(self):
        return f"ZeroAryityRelation: {self._name}  on {self._variables} "

    def __repr__(self):
        return f"ZeroAryityRelation({self._name}, {self._value})"

    def __hash__(self):
        return hash((self._name, self._value))

    def __eq__(self, other):
        if isinstance(other, ZeroAryityRelation):
            return self._name == other._name and self._value == other._value
        return False

    def __call__(self, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            return self._value
        raise ValueError("ZeroAryityRelation is only callable with empty arguments")

    def get_value_for_assignment(self, assignment: List[Any]) -> Any:
        if len(assignment) == 0:
            return self._value
        else:
            raise ValueError("ZeroAryityRelation only accepts empty assignment")

    def set_value_for_assignment(
        self, assignment: Dict[str, Any], relation_value
    ) -> "RelationProtocol":
        if len(assignment) == 0:
            return ZeroAryityRelation(self._name, relation_value)
        else:
            raise ValueError("ZeroAryityRelation only accepts empty assignment")

    def slice(self, partial_assignment: Dict[str, object]) -> "RelationProtocol":
        if len(partial_assignment) == 0:
            return self
        else:
            raise ValueError("ZeroAryityRelation only accepts empty assignment")
