from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation 
   
# initializing a figure in 
# which the graph will be plotted
fig = plt.figure() 
ax = fig.add_subplot()
x = np.array([0, 1, 2])
y = np.array([0, 1, 0])
ax.plot(x, y)

plt.show()