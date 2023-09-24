from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation 
import pandas as pd 

fig = plt.figure()
ax = fig.add_subplot()


print(np.array([[0,0],[1,1],[2,2]]).shape)
a = np.array([[1, 5],
              [2, 1]])
b = np.array([[4, 1],
              [2, 2]])
#print(np.matmul(a,b), np.matmul(b,a))
c = np.array([4,1,2,3])
d = np.array([5,1,2])

e = c[:,np.newaxis] + d[:]
print(e)

print(np.linalg.norm(e, axis = 1))
print(np.matmul(d[:,np.newaxis],c[np.newaxis,:]))

