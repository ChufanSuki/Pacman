import json

from pacman.infrastructure.orchestrator import RepairReadyMessage
from pacman.utils.simple_repr import simple_repr


def test_serialize_RepairReadyMessage():

    msg = RepairReadyMessage('a1', ['c1', 'c2', 'c3'])

    msg_repr = simple_repr(msg)
    json.dumps(msg_repr)