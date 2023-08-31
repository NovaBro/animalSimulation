import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlim([-5,5])
ax.set_ylim([-5,5])

class monster():
    def __init__(self, index) -> None:
        self.monsterIdentity = index
        self.speed = 0.01
        self.hitRadius = 0.25
        self.searchRadius = 1
        self.directionHeading = 0
        
    def goToPoint(self, point:list, globalPositions:np.ndarray):
        xDiff = point[0] - globalPositions[self.monsterIdentity][0]
        yDiff = point[1] - globalPositions[self.monsterIdentity][1]
        distance = np.sqrt(xDiff ** 2 + yDiff ** 2)
        newXposition = globalPositions[self.monsterIdentity][0] + self.speed * xDiff/distance
        newYposition = globalPositions[self.monsterIdentity][1] + self.speed * yDiff/distance
        if distance > self.hitRadius and -5 < newXposition < 5 and -5 < newYposition < 5:
            globalPositions[self.monsterIdentity] = np.array([newXposition, newYposition])
            self.directionHeading = np.arctan(yDiff/xDiff)

    def searchArea(self, globalPositions:np.ndarray):
        totalDirection = 0
        detected = 0
        for monster in globalPositions:
            xDiff = monster[0] - globalPositions[self.monsterIdentity][0]
            yDiff = monster[1] - globalPositions[self.monsterIdentity][1]
            distance = np.sqrt(xDiff ** 2 + yDiff ** 2)
            if distance < self.searchArea:
                detected += 1
                totalDirection += np.arctan(yDiff/xDiff)
        
        self.directionHeading = -(totalDirection/detected)
        


    def update(self, point:list, globalPositions:np.ndarray):
        self.goToPoint(point, globalPositions)


class food():
    def __init__(self) -> None:
        self.spawnPoint = [0, 0]
        self.speed = 0.10
        self.position = self.spawnPoint
        self.hitBoxRadius = 1
    
    def update():
        None

monsterCount = 10
allObjects = []
globalPositions = np.random.rand(monsterCount, 2) * 10 - 5
for i in range(monsterCount):
    monster1 = monster(i)
    allObjects.append(monster1)

def plotObjects(allObjects:list):
    allArtists = []
    for objectItem in allObjects:
        lineArtist, = ax.plot(globalPositions[objectItem.monsterIdentity][0], 
                              globalPositions[objectItem.monsterIdentity][1], '.b')
        allArtists.append(lineArtist)
    return allArtists

def animateFunction(i):
    print(i)
    for o in allObjects:
        o.update([1,1], globalPositions)

    return plotObjects(allObjects)

ani = animation.FuncAnimation(fig, animateFunction, frames=100, interval= 10, blit=True)
plt.show()