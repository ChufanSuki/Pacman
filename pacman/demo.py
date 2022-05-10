import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from pacman.computations_graph.pseudotree import _find_neighbors_relations, \
    _BuildingNode, \
    _generate_dfs_tree, _visit_tree, build_computation_graph, \
    _filter_relation_to_lowest_node, PseudoTreeNode, PseudoTreeLink, as_networkx_graph
from pacman.dcop.objects import Variable, VariableDomain
from pacman.dcop.dcop import DCOP
from pacman.dcop.relations import NAryFunctionRelation, relation_from_str
from pacman.utils.simple_repr import simple_repr, from_repr

# data = np.genfromtxt('metrics_cycle.csv', delimiter=',',
#                      names=['t', 'cycle', 'cost', 'violation' ,
#                             'msg_count', 'msg_size', 'status'])
#
# fig, ax = plt.subplots()
# ax.plot(data['t'], data['cost'], label='cost MGM')
# ax.set(xlabel='cycle', ylabel='cost')
# ax.grid()
# plt.title("MGM cost")
#
# fig.savefig("mgm_cost.png", bbox_inches='tight')
# plt.legend()
# plt.show()



# dcop = DCOP('test', 'min')
# d1 = VariableDomain('d1', '--', [1, 2, 3])
# v1 = Variable('v1', d1)
# v2 = Variable('v2', d1)
# c1 = relation_from_str('c1', '0.5 * v1 + v2', [v1, v2])
#
# dcop.add_constraint(c1)
#
# g = build_computation_graph(dcop)
# g1 = as_networkx_graph(g)
# pos = nx.spring_layout(g1)
# nx.draw(g1, with_labels=True, font_weight='bold')
# edge_labels = nx.get_edge_attributes(g1,'type')
# # nx.draw_networkx_edge_labels(g1, pos, labels=edge_labels)
# plt.show()

domain = ['a', 'b', 'c']
x1 = Variable('x1', domain)
x2 = Variable('x2', domain)
x3 = Variable('x3', domain)
variables = [x1, x2, x3]

r1 = NAryFunctionRelation(lambda x, y: x + y, [x1, x2], name='r1')
r2 = NAryFunctionRelation(lambda x, y: x + y, [x1, x3], name='r2')
r3 = NAryFunctionRelation(lambda x, y: x + y, [x2, x3], name='r3')
relations = [r1, r2, r3]

dcop = DCOP('test', 'min')
dcop.add_constraint(r1)
dcop.add_constraint(r2)
dcop.add_constraint(r3)

cg = build_computation_graph(dcop)
g1 = as_networkx_graph(cg)
pos = nx.spring_layout(g1)
nx.draw(g1, with_labels=True, font_weight='bold')
edge_labels = nx.get_edge_attributes(g1,'type')
# nx.draw_networkx_edge_labels(g1, pos, labels=edge_labels)
plt.show()