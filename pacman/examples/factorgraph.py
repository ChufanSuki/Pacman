import logging

from pacman.computations_graph.factor_graph import build_computation_graph
from pacman.dcop.yamldcop import load_dcop
from pacman.distribution.oneagent import distribute

logging.basicConfig(level=logging.DEBUG)
logging.info('SPEC Factor-graph')
import matplotlib.pyplot as plt

dcop_yaml = """
name: simple secp 1
objective: min
description: This is a very simple dcop modelling an secp with 3 light bulbs,
             1 models and one rule.

domains:
  luminosity:
    values: [0, 1, 2, 3, 4]
    type: 'luminosity'

variables:
# l1, l2 and l3 represent the 3 light bulb. They each have a different
# efficiency (from their cost function), l3 being the most efficient and l1
# the less efficient
  l1:
    domain: luminosity
    cost_function: 0.7 * l1
  l2:
    domain: luminosity
    cost_function: 0.5 * l2
  l3:
    domain: luminosity
    cost_function: 0.2 * l3

# m1 is the variable associated to the physical model that depends on l1, l2
 # and l2
  m1:
    domain: luminosity


constraints:
# m1_c is the contraint that bind the light bulb to the physical model
# variable m1
  m1_c:
    type: intention
    function: 0 if m1 == round(0.7 * l1 + 0.5 * l2 + 0.3 * l3) else 1000
# r1 is the constraint model the user rule: the target is to have a
# luminosity of 3 for the physical model and 2 for l2
  r1:
    type: intention
    function: 10 * (abs(m1 - 3) + abs(l2 -3))

agents:
# We have three agents one for each light bulb.
# The capacity is selected to make sure that all free computation cannot fit
# on one single agent.
  al1:
    capacity: 100
  al2:
    capacity: 100
  al3:
    capacity: 100

distribution_hints:
# For an secp, we have the additional constraint of hosting each light
# variable on the agent of the corresponding light bulb.
  must_host:
    al1: [l1]
    al2: [l2]
    al3: [l3]
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


pos = nx.spring_layout(graph)
nx.draw_networkx_nodes(graph, pos, nodelist=vnodes, node_shape='o')
nx.draw_networkx_nodes(graph, pos, nodelist=fnodes, node_shape='s')
nx.draw_networkx_edges(graph, pos)
nx.draw_networkx_labels(graph, pos)
# edge_labels = nx.get_edge_attributes(graph,'weight')
# nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
plt.show()