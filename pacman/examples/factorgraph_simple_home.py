import logging

from pacman.computations_graph.factor_graph import build_computation_graph
from pacman.dcop.yamldcop import load_dcop
from pacman.distribution.oneagent import distribute

logging.basicConfig(level=logging.DEBUG)
logging.info('SPEC Factor-graph')
import matplotlib.pyplot as plt

dcop_yaml = """

name: 'SimpleHouse'
description: This is a (manually converted) dcop representing the secp
  FullHouse.json.

objective: min

domains:
  light:
    values  : [0, 1, 2, 3, 4]
    type   : luminosity

variables:
  l_k1:
    domain : light
    initial_value: 0
    cost_function: l_k1 * 0.5
    noise_level: 0.2
  l_k2:
    domain : light
    initial_value: 0
    cost_function: l_k2 * 0.5
    noise_level: 0.2
  l_k3:
    domain : light
    initial_value: 0
    cost_function: l_k3 * 0.5
    noise_level: 0.2
  l_lv1:
    domain : light
    initial_value: 0
    cost_function: l_lv1 * 0.6
    noise_level: 0.2
  l_lv2:
    domain : light
    initial_value: 0
    cost_function: l_lv2 * 0.7
    noise_level: 0.2
  l_lv3:
    domain : light
    initial_value: 0
    cost_function: l_lv3 * 0.8
    noise_level: 0.2
  l_tv1:
    domain : light
    initial_value: 0
    cost_function: l_tv1 * 0.8
    noise_level: 0.2
  l_tv2:
    domain : light
    initial_value: 0
    cost_function: l_tv2 * 0.5
    noise_level: 0.2
  l_tv3:
    domain : light
    initial_value: 0
    cost_function: l_tv3 * 0.7
    noise_level: 0.2
  l_d1:
    domain : light
    initial_value: 0
    cost_function: l_d1 * 0.5
    noise_level: 0.2
  l_d2:
    domain : light
    initial_value: 0
    cost_function: l_d2 * 0.7
    noise_level: 0.2
  l_e1:
    domain : light
    initial_value: 0
    cost_function: l_e1 * 0.6
    noise_level: 0.2
  l_e2:
    domain : light
    initial_value: 0
    cost_function: l_e2 * 0.6
    noise_level: 0.2

  mv_kitchen:
    domain : light
    initial_value: 0
  mv_tv:
    domain : light
    initial_value: 0
  mv_livingroom:
    domain : light
    initial_value: 0
  mv_desk:
    domain : light
    initial_value: 0
  mv_entry:
    domain : light
    initial_value: 0
  mv_stairs:
    domain : light
    initial_value: 0


# Constraints
constraints:

  # Constraints for physical models
  mc_kitchen:
    type: intention
    function: 0 if 0.6 * l_k1 + 0.6 * l_k2 + 0.6 * l_k3 + 0.3 * l_lv2 + 0.3 * l_tv3 == mv_kitchen else 1000
  mc_tv:
    type: intention
    function: 0 if 0.2 * l_k1 + 0.3 * l_tv3 + 0.3 * l_tv2 + 0.4 * l_tv1 + 0.3 * l_lv2 + 0.2 * l_lv2 == mv_tv else 1000
  mc_livingroom:
    type: intention
    function: 0 if 0.2 * l_k1 + 0.5 * l_lv1 + 0.6 * l_lv2 + 0.5 * l_lv3 + 0.3 * l_d1 == mv_livingroom else 1000
  mc_desk:
    type: intention
    function: 0 if 0.7 * l_d1 + 0.5 * l_d2 + 0.3 * l_lv3 == mv_desk else 1000
  mc_entry:
    type: intention
    function: 0 if 0.7 * l_e1 + 0.3 * l_e2 == mv_entry else 1000
  mc_stairs:
    type: intention
    function: 0 if 0.3 * l_e1 + 0.7 * l_e2 == mv_stairs else 1000

  # Constraints for user-rules
  r_lunch:
    type: intention
    function: 10 * (abs(mv_livingroom - 5) + abs(mv_kitchen - 4))
  r_homecinema:
    type: intention
    function: 10 * (abs(mv_tv - 3) + abs(mv_kitchen - 1))
  r_work:
    type: intention
    function: 10 * (abs(mv_desk - 4))
  r_cooking:
    type: intention
    function: 10 * (abs(mv_kitchen - 4))
  r_entry:
    type: intention
    function: 10 * (abs(mv_entry - 4))


# Agents
agents:
  a_k1:
    capacity: 200
  a_k2:
    capacity: 200
  a_k3:
    capacity: 200
  a_lv1:
    capacity: 200
  a_lv2:
    capacity: 200
  a_lv3:
    capacity: 200
  a_tv1:
    capacity: 200
  a_tv2:
    capacity: 200
  a_tv3:
    capacity: 200
  a_d1:
    capacity: 200
  a_d2:
    capacity: 200
  a_e1:
    capacity: 200
  a_e2:
    capacity: 200


distribution_hints:

  must_host:
    # a pair agent_name : [list of variables or cconstraints names]
    # This means that computation dealing specificaly with one of these variable
    # or computation MUST be hosted on this agent.
    a_k1: [l_k1]
    a_k2: [l_k2]
    a_k3: [l_k3]
    a_lv1: [l_lv1]
    a_lv2: [l_lv2]
    a_lv3: [l_lv3]
    a_tv1: [l_tv1]
    a_tv2: [l_tv2]
    a_tv3: [l_tv3]
    a_d1: [l_d1]
    a_d2: [l_d2]
    a_e1: [l_e1]
    a_e2: [l_e2]

  host_with:
    # a pair variable name: list of constraint or variable names
    # of constraint name: list of constraint or variable names
    # indicates if the computation for this variable should be hosted on the
    # same agent as some other variables / agents.
    # This info is may be used by some distribution methods but not necessarily
    # all of them.
    mv_kitchen: [mc_kitchen]
    mv_livingroom: [mc_livingroom]
    mv_tv: [mc_tv]
    mv_desk: [mc_desk]
    mv_entry: [mc_entry]
"""
import networkx as nx

dcop = load_dcop(dcop_yaml)

cg = build_computation_graph(dcop)

graph = nx.Graph(type="factor-graph")
vnodes = []
fnodes = []
for node in cg.nodes:
    if node.type == "VariableComputation":
        vnodes.append(node.name)
    else:
        fnodes.append(node.name)

for node in vnodes:
    graph.add_node(node, s="o")

for node in fnodes:
    graph.add_node(node, s="^")

for link in cg.links:
    graph.add_edge(link.variable_node, link.factor_node)


pos = nx.nx_agraph.graphviz_layout(graph)
nx.draw_networkx_nodes(graph, pos, nodelist=vnodes, node_shape='o')
nx.draw_networkx_nodes(graph, pos, nodelist=fnodes, node_shape='s')
nx.draw_networkx_edges(graph, pos)
nx.draw_networkx_labels(graph, pos)
# edge_labels = nx.get_edge_attributes(graph,'weight')
# nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
plt.show()
nx.write_gexf(graph, "test.gexf")