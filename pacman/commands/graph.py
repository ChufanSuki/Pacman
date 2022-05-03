
"""
.. _pacman_commands_graph:

pacman graph
============

``pacman graph`` outputs some metrics for a graph model for a DCOP.

Synopsis
--------
::

  pacman graph --graph <graph_model> <dcop_files>


Description
-----------

Outputs some metrics for a graph model for a DCOP:

* constraints_count
* variables_count
* density
* edges_count
* nodes_count


Options
-------

``--graph <graph_model>`` / ``-g <graph_model>``
  The computation graph model,
  one of ``factor_graph``, ``pseudotree``, ``constraints_hypergraph``
  (see. :ref:`concepts_graph`)
  The set of computation to distribute depends on the graph model used to
  represent the DCOP.

``--display``
  Display a graphical representation of the constraints graph using
  networkx and matplotlib.

``<dcop-files>``
  One or several paths to the files containing the dcop. If several paths are
  given, their content is concatenated as used a the yaml definition for the
  DCOP.


Example
-------

::

  pacman graph --graph factor_graph graph_coloring1.yaml

Example output::

  constraints_count: 2
  density: 0.4
  edges_count: 4
  nodes_count: 5
  status: OK
  variables_count: 3



"""

import logging
from importlib import import_module
import sys
import yaml

from pacman.dcop.yamldcop import load_dcop_from_file
from pacman.utils.graphs import (
    as_networkx_graph,
    display_graph,
    display_bipartite_graph,
)

logger = logging.getLogger("pacman.cli.graph")


# TODO : ass more graph metrics:
# * number of cycles
# * is connected ?
# * number of sub-graph (if not connected)


def set_parser(subparsers):

    parser = subparsers.add_parser(
        "graph",
        help="Graph metrics for dcop graphs. Can also be used to display a graphical "
        "representation of the graph.",
    )
    parser.set_defaults(func=run_cmd)

    parser.add_argument("dcop_file", type=str, nargs="+", help="dcop file(s)")

    parser.add_argument(
        "--display",
        default=False,
        action="store_true",
        help="Display the constraints graph using networkx and " "matplotlib",
    )
    parser.add_argument(
        "-g",
        "--graph",
        choices=["factor_graph", "pseudotree", "constraints_hypergraph"],
        help="graphical model for dcop computations",
    )


def run_cmd(args):
    logger.debug('dcop command "graph" with arguments {} '.format(args))

    dcop_yaml_file = args.dcop_file
    logger.info("loading dcop from {}".format(dcop_yaml_file))
    dcop = load_dcop_from_file(dcop_yaml_file)

    if args.display:
        if args.graph == "factor_graph":
            display_bipartite_graph(dcop.variables.values(), dcop.constraints.values())
        else:
            display_graph(dcop.variables.values(), dcop.constraints.values())

    try:
        graph_module = import_module("pacman.computations_graph.{}".format(args.graph))
        logger.info("Building computation graph for dcop {}".format(dcop.name))
        graph_stats(dcop, graph_module)
    except ImportError:
        _error("Could not find computation graph type: {}".format(args.graph))


def graph_stats(dcop, graph_module):

    # Build factor-graph computation graph
    logger.info("Building computation graph for dcop {}".format(dcop.name))
    cg = graph_module.build_computation_graph(dcop)

    edges_count = len(list(cg.links))
    nodes_count = len(list(cg.nodes))
    density = cg.density()

    # TODO: add other graph metrics :
    # branching factor
    # diameter
    # number or loops
    # root (when it's a tree)
    # # variables and # factors, when it's a factor graph

    # Note : when using variables with integrated costs, the costs factors
    # are not accounted for in the metrics.

    result = {
        "status": "OK",
        "variables_count": len(dcop.variables),
        "constraints_count": len(dcop.constraints),
        "nodes_count": nodes_count,
        "edges_count": edges_count,
        "density": density,
    }
    print(yaml.dump(result, default_flow_style=False))


def _error(msg):
    print("Error: {}".format(msg))
    sys.exit(2)
