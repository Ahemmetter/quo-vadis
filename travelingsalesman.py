# import statements
import csv
import random
import numpy as np
import copy
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# reads csv file with sights and their data

filename = "testsights.csv"
with open(filename, "r") as f:
    reader = csv.reader(f, delimiter=";")
    next(reader, None)                          # skips header row
    sights = [row for row in reader]
    for row in sights:
        for i in [2, 3, 4]:                     # these columns contain floats
            row[i] = float(row[i])

# constants
picks = 7                                       # number of sights to be visited + 1
hotel = ["hotel", "spb", 1.0, 662.0, 457.0]     # data of hotel
sights.append(hotel)                            # adds hotel to the sights
l = len(sights)
ordered = np.arange(l-1)                        # lists all sights in order to be picked from without hotel
tour = sorted(random.sample(ordered, picks))    # samples "picks" number of sights from the ordered list
tour.append(l-1)                                # appends hotel as last index in tour
bestTour = tour                                 # keeps track of the shortest tour so far
bestd = 9999999                                 # maximum total distance

def distance(n, m):
    # calculates distance between two points

    x1, y1 = sights[n][3], sights[n][4]         # coordinates of the sights
    x2, y2 = sights[m][3], sights[m][4]
    dist = np.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2)
    return dist

for T in np.logspace(0, 5, num = 10000)[::-1]:
    # decreases temperature in logarithmic steps

    od = 0                                      # distances from the previous tour
    for n in range(picks+1):
        # calculates the total distance of the tour

        if n != picks:
            od = od + distance(tour[n], tour[n+1])
        elif n == picks:
            od = od + distance(tour[n], tour[0])

    # picks two random sights and swaps them
    [i, j] = sorted(random.sample(np.arange(picks+1), 2))
    newTour = tour                              # this is called a new tour
    newTour[i], newTour[j] = tour[j], tour[i]

    nd = 0                                      # total distance of the new tour
    for n in range(picks+1):
        # is calculated just like previously
        if n != picks:
            nd = nd + distance(newTour[n], newTour[n+1])
        elif n == picks:
            nd = nd + distance(newTour[n], newTour[0])

    if nd < bestd:
        # if the new distance is better than the old (shorter), then accept it
        bestTour = tour
        bestd = nd

    if od - nd > 0:
        # if new tour is shorter, accept it
        tour = copy.copy(newTour)
    elif np.exp((od - nd)/T) > random.random():
        # if it is not shorter, randomly accept it, if the jumps are small enough
            tour = copy.copy(newTour)
    else:
        # otherwise reject it and keep the old path
        nd = od
        newTour = tour

# assemble the tour and print them in the console
visit = []
print bestTour
for i in bestTour:
    visit.append(sights[i][0])
print visit                                     # print sights in order
print bestd                                     # print total tour length

# collect coordinates for the plot
xb = []
yb = []

for i in range(picks+1):
    xb.append(sights[bestTour[i]][3])
    yb.append(sights[bestTour[i]][4])
xb.append(sights[bestTour[0]][3])
yb.append(sights[bestTour[0]][4])

# plot statements
plt.plot(xb, yb, "xr-", linewidth = 3)          # plots tour
plt.plot(hotel[3], hotel[4], "og")              # sets a marker for the hotel
plt.xlim(0, 807)
plt.ylim(521, 0)
plt.gca().set_aspect('equal', adjustable='box') # keeps aspect ratio

image = mpimg.imread("spbmap.png")              # allows the plot to be overlaid over the map
plt.imshow(image)
plt.show()
