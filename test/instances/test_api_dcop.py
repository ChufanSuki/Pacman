

from pacman.dcop.dcop import DCOP
from pacman.dcop.objects import Domain, create_variables

"""
Tests for the DCOP API.

Creating various kind of DCOP using the api.

"""


def test_api_dcop_graph_coloring():

    # Graph coloring with 3 variables and color preferences

    dcop = DCOP('test')

    # Domain and variables
    d = Domain('color', '', ['R', 'G'])
    variables = create_variables('v', [1, 2, 3], d)

    # Creating constraints using the convenience += notation
    # We could also use the more verbose dcop.add_constraint method.
    # Variable(s) and domain(s) involved in the constraint are automatically
    # added to the dcop.
    # unary constraints for preferences
    dcop += 'cost_1', '-0.1 if v1 == "R" else 0.1 ', variables
    dcop += 'cost_2', '-0.1 if v2 == "G" else 0.1 ', variables
    dcop += 'cost_3', '-0.1 if v3 == "G" else 0.1 ', variables
    # coloring constraints : v1 != v2 != v3
    dcop += 'c1', '1 if v1 == v2 else 0', variables
    dcop += 'c2', '1 if v3 == v2 else 0', variables

    # let's check the dcop really has all required domain, variables and
    # constraints
    assert len(dcop.variables) == 3
    assert 'v1' in dcop.variables

    assert len(dcop.domains) == 1
    assert 'color' in dcop.domains

    assert len(dcop.constraints) == 5
    assert 'cost_3' in dcop.constraints
    assert 'c2' in dcop.constraints
