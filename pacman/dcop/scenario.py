

from typing import List

from pacman.utils.simple_repr import SimpleRepr


class EventAction(SimpleRepr):

    def __init__(self, type: str, **kwargs):
        self._type = type
        self._args = kwargs

    @property
    def type(self):
        return self._type

    @property
    def args(self):
        return self._args

    def __repr__(self):
        return 'EventAction({}, {})'.format(self.type, self._args)


class DcopEvent(SimpleRepr):
    """
    A Dcop Event is used to represent an event happening in the system.

    An event can contains several actions that are happening at the same time.
    This is for example useful when several agents disappear simultaneously.

    """

    type = None

    def __init__(self, id: str, delay: float =None,
                 actions: List[EventAction] =None):
        """
        :param actions: a list of EventAction objects
        """
        self._actions = actions
        self._delay = delay
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def delay(self):
        return self._delay

    @property
    def actions(self):
        return self._actions

    @property
    def is_delay(self):
        return self.delay is not None

    def __repr__(self):
        return 'Event({}, {})'.format(self.id, self.actions)


class Scenario(SimpleRepr):
    """
    A scenario is a list of events that happens in the system.

    """
    def __init__(self, events: List[DcopEvent]= None):

        self._events = events if events else []

    def __iter__(self):
        return iter(self._events)

    @property
    def events(self):
        return list(self._events)