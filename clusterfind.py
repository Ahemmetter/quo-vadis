import numpy as np
import random
import matplotlib.pyplot as plt

x = []
y = []
for i in range(10):
    x.append(random.randrange(1,91,1))
    y.append(random.randrange(1,91,1))

def distance(n, m):
    x1, y1 = x[n], y[n]
    x2, y2 = x[m], y[m]
    dist = np.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)
    return dist

def distcenter(centerx, centery, n):
    x1, y1 = x[n], y[n]
    distfromcenter = np.sqrt(abs(centerx-x1)**2 + abs(centery-y1)**2)
    return distfromcenter

max = 0
n0 = 0
m0 = 0
n1 = 0
for n in range(10):
    for m in range(10):
        if distance(n, m) > max:
            max = distance(n, m)
            n0 = n
            m0 = m

radius = 0.5*max
centerx = 0.5*abs(x[n0] + x[m0])
centery = 0.5*abs(y[n0] + y[m0])

maxradius = radius
for n in range(10):
    if distcenter(centerx, centery, n) > maxradius:
        maxradius = distcenter(centerx, centery, n)
        n1 = n

fig, ax = plt.subplots()
circle = plt.Circle((centerx, centery), maxradius, color='b', fill=False)

ax.plot(x, y, 'ro')
ax.plot([x[n0], x[m0]], [y[n0], y[m0]], "g")
plt.xlim(-45, 135)
plt.ylim(-45, 135)
plt.gca().set_aspect('equal', adjustable='box')
ax.grid()
ax.add_artist(circle)
plt.show()
