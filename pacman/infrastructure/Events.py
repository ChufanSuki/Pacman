"""
very simple event-bux mechanism.

"""
from collections import defaultdict
from functools import wraps
from typing import Callable


class EventDispatcher(object):
    """
    A very simple event dispatcher.

    """

    def __init__(self, enabled=False):
        self._cbs = defaultdict(lambda: [])
        self.enabled = enabled

    def send(self, topic, evt):
        if not self.enabled:
            return
        for cb in self._cbs[topic]:
            cb(topic, evt)
        all_cbs = list(self._cbs.items())
        eligibles = [
            cbs
            for s_topic, cbs in all_cbs
            if s_topic[-1] == "*" and topic.startswith(s_topic[:-1])
        ]
        for cbs in eligibles:
            for cb in cbs:
                cb(topic, evt)

    def subscribe(self, topic: str, cb: Callable):
        """
        Register a call back to topic.

        Parameters
        ----------
        topic: str
            a topic
        cb:
            a callback

        Returns
        -------
        callable:
            The registered callback.
        """
        self._cbs[topic].append(cb)
        return cb

    def unsubscribe(self, cb: Callable, topic: str = None):

        if topic is None:
            all_cbs = list(self._cbs.items())
            for s_topic, s_cbs in all_cbs:
                if cb in s_cbs:
                    s_cbs.remove(cb)
        # else:

    def reset(self):
        self._cbs.clear()


event_bus = EventDispatcher()

buses = defaultdict(lambda: EventDispatcher())


def get_bus(name: str):
    return buses[name]
