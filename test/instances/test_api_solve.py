
from pacman.dcop.objects import create_agents
from pacman.infrastructure.run import solve
from test.instances.instance import dcop_graphcoloring_3


def test_api_solve_maxsum():

    dcop = dcop_graphcoloring_3()
    # Agents
    dcop.add_agents(create_agents('a', [1, 2, 3], capacity=50))

    assignment = solve(dcop, 'maxsum','adhoc', timeout=3)

    check_suboptimal_result(assignment)

def test_api_solve_dsa():

    dcop = dcop_graphcoloring_3()
    dcop.add_agents(create_agents('a', [1, 2, 3], capacity=50))

    assignment = solve(dcop, 'dsa','oneagent', timeout=3)

    check_suboptimal_result(assignment)


def test_api_solve_dsatuto():

    dcop = dcop_graphcoloring_3()
    dcop.add_agents(create_agents('a', [1, 2, 3], capacity=50))

    assignment = solve(dcop, 'dsatuto','oneagent', timeout=3)

    check_suboptimal_result(assignment)


def test_api_solve_mgm():

    dcop = dcop_graphcoloring_3()
    dcop.add_agents(create_agents('a', [1, 2, 3], capacity=50))

    assignment = solve(dcop, 'mgm','oneagent', timeout=3)

    check_suboptimal_result(assignment)


def test_api_solve_mgm2():

    dcop = dcop_graphcoloring_3()
    dcop.add_agents(create_agents('a', [1, 2, 3], capacity=50))

    assignment = solve(dcop, 'mgm2','oneagent', timeout=3)

    check_suboptimal_result(assignment)


def test_api_solve_dpop():

    dcop = dcop_graphcoloring_3()
    dcop.add_agents(create_agents('a', [1, 2, 3], capacity=50))

    assignment = solve(dcop, 'dpop','oneagent', timeout=3)

    check_optimal_result(assignment)


def check_optimal_result(assignment):
    assert assignment == {'v1': 'R', 'v2': 'G', 'v3': 'R'}

def check_suboptimal_result(assignment):
    # An incomplete algo does not always find the best solution but
    # finds one of two solution that does not break hard constraints.
    one_of_two = (assignment == {'v1': 'R', 'v2': 'G', 'v3': 'R'}) or \
           (assignment == {'v1': 'G', 'v2': 'R', 'v3': 'G'})
    assert one_of_two
