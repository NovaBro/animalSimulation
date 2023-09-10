import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot()
ax.set_xlim([-6,6])
ax.set_ylim([-6,6])

class monster():
    def __init__(self, index) -> None:
        self.monsterIdentity = index
        self.speed = 0.01
        self.hitRadius = 1
        self.searchRadius = 1
        self.directionHeading = 0

        
    def goToPoint(self, point:list, globalPositions:np.ndarray):
        xDiff = point[0] - globalPositions[self.monsterIdentity][0]
        yDiff = point[1] - globalPositions[self.monsterIdentity][1]
        distance = np.sqrt(xDiff ** 2 + yDiff ** 2)
        newXposition = globalPositions[self.monsterIdentity][0] + self.speed * xDiff/distance
        newYposition = globalPositions[self.monsterIdentity][1] + self.speed * yDiff/distance
        if -5 < newXposition < 5 and -5 < newYposition < 5:
            globalPositions[self.monsterIdentity] = np.array([newXposition, newYposition])
        else:
            #print(self.directionHeading)
            self.directionHeading += np.pi
            #print(self.directionHeading)


    def distanceCalculation(self, x, y):
        return np.sqrt(x ** 2 + y ** 2)
    
    def calculatePoint(self, populationDirection, avgHeading, influenceFactor):
        goDirection = (populationDirection + avgHeading) * influenceFactor + self.directionHeading
        self.directionHeading = goDirection
        return [np.cos(goDirection), np.sin(goDirection)] 
        
        


    def searchArea(self, globalPositions:np.ndarray, allObjects:list):
        totalXDiff = 0
        totalYDiff = 0
        searchCount = 0
        avgXDis = 0
        avgYDis = 0
        avgHeading = 0


        for i in range(len(globalPositions)):
            xDiff = globalPositions[i][0] - globalPositions[self.monsterIdentity][0]
            yDiff = globalPositions[i][1] - globalPositions[self.monsterIdentity][1]

            distance = self.distanceCalculation(xDiff, yDiff)
            if distance < self.searchRadius:
                totalXDiff += xDiff
                totalYDiff += yDiff
                searchCount += 1
                avgHeading += allObjects[i].directionHeading
        
        if searchCount != 0:
            avgXDis = totalXDiff / searchCount
            avgYDis = totalYDiff / searchCount
            avgHeading /= searchCount

        influenceFactor = 0.001
        if self.distanceCalculation(avgXDis, avgYDis) < self.hitRadius:
            populationDirection = np.arctan(avgYDis/avgXDis) + np.pi
            self.goToPoint(self.calculatePoint
                           (populationDirection, avgHeading, influenceFactor), globalPositions)

        else:
            populationDirection = np.arctan(avgYDis/avgXDis)
            self.goToPoint(self.calculatePoint
                           (populationDirection, avgHeading, influenceFactor), globalPositions)

    def update(self, globalPositions:np.ndarray, allObjects:list):
        self.searchArea(globalPositions, allObjects)

        #self.goToPoint(point, globalPositions)

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
    #print(i)
    for o in allObjects:
        o.update(globalPositions, allObjects)
        for m in allObjects:
            print(m.directionHeading)

    return plotObjects(allObjects)

ani = animation.FuncAnimation(fig, animateFunction, frames=1000, interval= 10, blit=True)
plt.show()