from pacman.dcop.objects import AgentDef, create_agents


def test_api_create_agent_minimal():

    # The name is the only mandatory param when creating an agent definition?
    a1 = AgentDef('a1')

    assert a1.name == 'a1'
    # Defaults values for route and hosting costs:
    assert a1.route('a_foo') == 1
    assert a1.hosting_cost('computation_bar') == 0


def test_api_create_agent_with_default_cost():

    a1 = AgentDef('a1', default_route=10, default_hosting_cost=5)

    assert a1.name == 'a1'
    # Defaults values for route and hosting costs:
    assert a1.route('a_foo') == 10
    assert a1.hosting_cost('computation_bar') == 5


def test_api_create_agent_with_specific_cost_as_dict():

    a1 = AgentDef('a1', routes={'a2': 8},
                  hosting_costs={'c1': 3})

    assert a1.name == 'a1'
    # Specific and defaults values for route and hosting costs:
    assert a1.route('a_foo') == 1
    assert a1.route('a2') == 8
    assert a1.hosting_cost('c1') == 3
    assert a1.hosting_cost('computation_bar') == 0


def test_api_create_several_agents():

    agents = create_agents('a', [1, 2, 3])
    assert agents['a1'].name == 'a1'
    assert 'a3' in agents


    # Agents
    # TODO : use callable for hosting and route ?

