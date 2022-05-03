from time import sleep
from unittest.mock import MagicMock

import pytest

from pacman.algorithms import AlgorithmDef, ComputationDef
from pacman.computations_graph.constraints_hypergraph import \
    VariableComputationNode
from pacman.dcop.objects import AgentDef, Variable
from pacman.infrastructure.communication import InProcessCommunicationLayer
from pacman.infrastructure.computations import MessagePassingComputation
from pacman.infrastructure.orchestrator import DeployMessage, RunAgentMessage, \
    PauseMessage, StopAgentMessage
from pacman.infrastructure.orchestratedagents import OrchestratedAgent


################################################################################
#  Tests Fixtures

@pytest.fixture
def orchestrated_agent():
    a1_def = AgentDef('a1')
    fake_address = MagicMock()
    agt = OrchestratedAgent(a1_def, InProcessCommunicationLayer(),
                            fake_address)
    # As we don't create an orchestrator, catch message sending
    agt._messaging.post_msg = MagicMock()
    yield agt
    agt.stop()


################################################################################
# Tests cases


def test_start_orchestrated_agent_starts_mgt(orchestrated_agent):
    # Check the management computation is started when stating the
    # OrchestratedAgent
    assert not orchestrated_agent.is_running
    orchestrated_agent.start()
    sleep(0.1)
    assert orchestrated_agent.is_running
    assert orchestrated_agent._mgt_computation.is_running
    assert orchestrated_agent._mgt_computation.name == '_mgt_a1'
    assert orchestrated_agent._mgt_computation.footprint() == 0


def test_deploy_computation_request(orchestrated_agent):
    orchestrated_agent.start()
    orchestrated_agent.add_computation = MagicMock()

    mgt = orchestrated_agent._mgt_computation
    v1 = Variable('v1', [1, 2, 3])
    comp_node = VariableComputationNode(v1, [])
    comp_def = ComputationDef(
        comp_node, AlgorithmDef.build_with_default_param('dsa'))
    mgt.on_message('orchestrator', DeployMessage(comp_def), 0)

    # Check the computation is deployed, but not started, on the agent
    calls = orchestrated_agent.add_computation.mock_calls
    assert len(calls) == 1
    _, args, _ = calls[0]
    computation = args[0]
    assert isinstance(computation, MessagePassingComputation)
    assert not computation.is_running


def test_run_computations(orchestrated_agent):

    orchestrated_agent.start()
    mgt = orchestrated_agent._mgt_computation
    orchestrated_agent.run = MagicMock()

    computations = ['c1', 'c2', 'c3']
    mgt.on_message('orchestrator', RunAgentMessage(computations), 0)

    orchestrated_agent.run.assert_called_once_with(
        ['c1', 'c2', 'c3'])


def test_pause_computations(orchestrated_agent):

    orchestrated_agent.start()
    mgt = orchestrated_agent._mgt_computation
    orchestrated_agent.pause_computations = MagicMock()

    computations = ['c1', 'c2', 'c3']
    mgt.on_message('orchestrator', PauseMessage(computations), 0)

    orchestrated_agent.pause_computations.assert_called_once_with(
        ['c1', 'c2', 'c3'])


def test_stop_agent(orchestrated_agent):
    orchestrated_agent.start()
    mgt = orchestrated_agent._mgt_computation
    # Do NOT mock the stop method, otherwise the agent will never stop !
    # orchestrated_agent.stop = MagicMock()

    mgt.on_message('orchestrator', StopAgentMessage(), 0)

    sleep(0.1)
    assert not orchestrated_agent.is_running
