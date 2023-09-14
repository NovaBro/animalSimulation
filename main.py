import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot()
windowSize = 5
ax.set_xlim([-windowSize,windowSize])
ax.set_ylim([-windowSize,windowSize])

class monster():
    def __init__(self, index, speed, hitRadius, searchRadius, separationFactor, headingFactor) -> None:
        self.monsterIndex = index
        self.speed = speed
        self.hitRadius = hitRadius
        self.searchRadius = searchRadius
        self.directionHeading = np.random.random() * 2 * np.pi
        self.separationFactor = separationFactor
        self.headingFactor = headingFactor


    def findDistance(self, globalPositions, monster1Index, monster2Index):
        xdif = globalPositions[monster1Index][0] - globalPositions[monster2Index][0]
        ydif = globalPositions[monster1Index][1] - globalPositions[monster2Index][1]
        return np.sqrt(xdif**2 + ydif**2)

    def findNeighbors(self, globalPositions, allObjects):
        neighboring = []
        for index in range(len(globalPositions)):
            if self.findDistance(globalPositions, index, self.monsterIndex) < self.searchRadius:
                neighboring.append(allObjects[index].monsterIndex)
        return neighboring
    
    def distanceTOangle(self, xDiff, yDiff, opposite):
        "If Opposite is 1, then go in the opposite direction. 0 goes in same direction"
        if opposite == 1:
            if (xDiff > 0 and yDiff > 0):
                self.directionHeading = np.pi + np.arctan(yDiff/xDiff)
            elif xDiff > 0:
                self.directionHeading = np.pi + np.arctan(yDiff/xDiff)
            elif yDiff > 0:
                self.directionHeading = np.arctan(yDiff/xDiff)
            else:
                self.directionHeading = np.arctan(yDiff/xDiff)
        elif opposite == 0:
            if (xDiff > 0 and yDiff > 0):
                self.directionHeading = np.arctan(yDiff/xDiff)
            elif xDiff > 0:
                self.directionHeading = np.arctan(yDiff/xDiff)
            elif yDiff > 0:
                self.directionHeading = np.pi + np.arctan(yDiff/xDiff)
            else:
                self.directionHeading = np.pi + np.arctan(yDiff/xDiff)
    
    def moveInHeading(self, globalPositions):
        
        if -5 < globalPositions[self.monsterIndex][0] < 5 and \
           -5 < globalPositions[self.monsterIndex][1] < 5:
            print(f"Before Direction: {self.directionHeading * 180 / np.pi}")
            xChange = np.cos(self.directionHeading)
            yChange = np.sin(self.directionHeading)
            globalPositions[self.monsterIndex][0] += self.speed * xChange
            globalPositions[self.monsterIndex][1] += self.speed * yChange
            print(f"Still Good, {self.directionHeading * 180 / np.pi}")
        else:
            print(f"Before Direction: {self.directionHeading * 180 / np.pi}")
            xDiff = globalPositions[self.monsterIndex][0]
            yDiff = globalPositions[self.monsterIndex][1]
            
            self.distanceTOangle(xDiff, yDiff, 1)

            print(f"After Change: {self.directionHeading * 180 / np.pi}, Ydiff {yDiff}, Xdiff {xDiff}")
            xChange = np.cos(self.directionHeading)
            yChange = np.sin(self.directionHeading)
            globalPositions[self.monsterIndex][0] += self.speed * xChange
            globalPositions[self.monsterIndex][1] += self.speed * yChange
            print(f"After Change, {self.directionHeading * 180 / np.pi}")

    def findcenter(self, neighbors, globalPositions):
        xPositionAvg = 0
        yPositionAvg = 0
        for i in neighbors:
            xPositionAvg += globalPositions[i][0]
            yPositionAvg += globalPositions[i][1]
        xPositionAvg /= len(neighbors)
        yPositionAvg /= len(neighbors)

        return [xPositionAvg, yPositionAvg]
    
    def SeparationAndCohesion(self, center, globalPositions, importanceFactor):
        "Importance factor decides how much weight to assign to the neighbor center"
        xPosition = globalPositions[self.monsterIndex][0]
        yPosition = globalPositions[self.monsterIndex][1]
        xdif = center[0] - xPosition
        ydif = center[1] - yPosition
        distance = np.sqrt(xdif**2 + ydif**2)

        if distance <= self.hitRadius:
            currentX = np.cos(self.directionHeading) - xdif * importanceFactor
            currentY = np.sin(self.directionHeading) - ydif * importanceFactor
            self.distanceTOangle(currentX, currentY, 0)
        else:
            currentX = np.cos(self.directionHeading) + xdif * importanceFactor
            currentY = np.sin(self.directionHeading) + ydif * importanceFactor
            self.distanceTOangle(currentX, currentY, 0)


    def findHeadings(self, neighbors, allObjects):
        averageHeading = 0
        for i in neighbors:
            averageHeading += allObjects[i].directionHeading
        averageHeading /= len(neighbors)
        return averageHeading

    def update(self, globalPositions, allObjects):
        neighboring = self.findNeighbors(globalPositions, allObjects)
        center = self.findcenter(neighboring, globalPositions)

        self.SeparationAndCohesion(center, globalPositions, self.separationFactor)

        averageTheta = self.findHeadings(neighboring, allObjects)
        currentX = np.cos(self.directionHeading) + np.cos(averageTheta) * self.headingFactor
        currentY = np.sin(self.directionHeading) + np.sin(averageTheta) * self.headingFactor
        self.distanceTOangle(currentX, currentY, 0)

        self.moveInHeading(globalPositions)


monsterCount = 20
speed = 0.02
hitRadius = 0.2
searchRadius = 0.75
separationCohesionFactor = 0.5
headingFactor = 0.01

allObjects = []
globalPositions = np.random.rand(monsterCount, 2) * 10 - 5
for i in range(monsterCount):
    monster1 = monster(i, speed, hitRadius, searchRadius, separationCohesionFactor, headingFactor)
    allObjects.append(monster1)

def plotObjects(allObjects:list):
    allArtists = []
    for objectItem in allObjects:
        lineArtist, = ax.plot(globalPositions[objectItem.monsterIndex][0], 
                              globalPositions[objectItem.monsterIndex][1], '.b')
        allArtists.append(lineArtist)
    return allArtists

def animateFunction(i):
    #print(i)
    for o in allObjects:
        o.update(globalPositions, allObjects)
        print("----------")
        #for m in allObjects:
        #    print(m.directionHeading / np.pi * 180)

    return plotObjects(allObjects)

ani = animation.FuncAnimation(fig, animateFunction, frames=1000, interval= 10, blit=True)
plt.show()