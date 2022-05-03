"""Various utils and tests instances for API testing.

"""
from pacman.dcop.dcop import DCOP
from pacman.dcop.objects import Domain, create_variables


def dcop_graphcoloring_3():
    """
    Build a simple 3-variable graph coloring problem.

    v1--v2--v3

    Each variable has a cost function which makes it prefer one color:
    v1 prefers R
    v2 prefers G
    v3 prefers G

    Of course, the preferences of v2 and v3 conflict.
    The best affectation is
    v1 - R
    v2 - G
    v3 - R

    Returns
    -------

    """
    dcop = DCOP('graphcoloring_3')
    # Domain and variables
    d = Domain('color', '', ['R', 'G'])
    variables = create_variables('v', ['1', '2', '3'], d)
    # unary constraints for preferences
    dcop += 'cost_1', '-0.1 if v1 == "R" else 0.1 ', variables
    dcop += 'cost_2', '-0.1 if v2 == "G" else 0.1 ', variables
    dcop += 'cost_3', '-0.1 if v3 == "G" else 0.1 ', variables
    # coloring constraints : v1 != v2 != v3
    dcop += 'c1', '1 if v1 == v2 else 0', variables
    dcop += 'c2', '1 if v3 == v2 else 0', variables

    # Note that we do not define the agents for this dcop here,
    # as the number of agents depends on the test case we will use the dcop for.

    return dcop