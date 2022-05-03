import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt('metrics_cycle.csv', delimiter=',',
                     names=['t', 'cycle', 'cost', 'violation' ,
                            'msg_count', 'msg_size', 'status'])

fig, ax = plt.subplots()
ax.plot(data['t'], data['cost'], label='cost MGM')
ax.set(xlabel='cycle', ylabel='cost')
ax.grid()
plt.title("MGM cost")

fig.savefig("mgm_cost.png", bbox_inches='tight')
plt.legend()
plt.show()