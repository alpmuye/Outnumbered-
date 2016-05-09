
from helperFunctions import *

from MapItems import *

########### Helper Functions for Maze Solver
def doesPointIntersectWithSoldiers(testPoint, data, Warrior): 
		for otherWarrior in data.Warriors:
			if otherWarrior==Warrior: continue #that's me yo.
			point1=testPoint
			point2=(otherWarrior.x, otherWarrior.y)
			distance=getDistance((point1), (point2))
			if (otherWarrior.radius*2.1)>=distance:
				return True
		return False

def doesPointIntersectWithObstacles(testPoint, data, radius):
	for item in data.Map.items:
		if doesPointIntersectWithItem(testPoint, radius, item):
			if item.isMovable: continue
			return True
	return False

def isPathClearTestPoints(position, target):
	testPoints=[target]
	(targetX, targetY)=target #unpacking.
	(positionX, positionY)=position
	deltaX=targetX-positionX
	deltaY=targetY-positionY
	angle=getAngleFromDeltas(deltaX, deltaY)
	step=10
	(incrementX, incrementY)=balanceVelocityIntoVectors(step, angle)
	(testPointX, testPointY)=(positionX+incrementX,
									positionY+incrementY)
	while not closeEnoughMaze(target, (testPointX, testPointY)):
		testPoints.append((testPointX,testPointY))
		testPointX+=incrementX
		testPointY+=incrementY
	return testPoints

def isThereObstacleInSight(self, BlueWarrior, Warrior): #self is the data.
	deltaX=Warrior.x-BlueWarrior.x
	deltaY=Warrior.y-BlueWarrior.y 
	angle=getAngleFromDeltas(deltaX, deltaY)
	step=2
	(incrementX, incrementY)=balanceVelocityIntoVectors(step, angle)
	(testPointX, testPointY)=(BlueWarrior.x+incrementX,
								 BlueWarrior.y+incrementY)
	while not Warrior.contains(testPointX,testPointY):
		for item in self.Map.items:
			if item.contains(testPointX, testPointY):
				return True
		testPointX+=incrementX
		testPointY+=incrementY
	return False #direct connection to enemy Warrior.

def isPathClear(position, target, data, Warrior):
	testPoints=isPathClearTestPoints(position, target)
	listed=[]
	for testPointI in range(len(testPoints)-1):
		listed.append(testPoints[testPointI][0])
	if sorted(listed)==listed: return False #fixes empty list bug.
	for testPoint in testPoints:
		if doesPointIntersectWithSoldiers(testPoint, data, Warrior):
			return False
		elif doesPointIntersectWithObstacles(testPoint, data, Warrior.radius):
			return False
	return True 

###########

#AI for resolving obstacles, and troop intersections

class MazeSolver(object):

	@staticmethod
	def solveMazeHelper(Warrior, data): #Adapted/inspired from Maze Solver of 
		visited = []					#recursion part 2 class-notes.
		targetX,targetY = Warrior.destinations[0]
		def solve(x,y, limit=1):
		    # base cases
			if (x,y) in visited: return False
			if len(visited)>limit: return False
			visited.append((x,y))
			if isPathClear((x,y), (targetX,targetY), data, Warrior):
				return True
			# recursive case
			increment=Warrior.radius*3
			dirs  = [ (-increment, -increment), (-increment, 0), 
					(-increment, increment), ( 0, -increment),( 0, increment), 
					(increment, -increment), (increment, 0), 
					(increment, increment)] 
			for direction in dirs:
				(deltaX, deltaY)=direction
				if isPathClear((x,y), (x+deltaX,y+deltaY), data, Warrior):
					if solve(x+deltaX,y+deltaY, limit): return True
			visited.remove((x,y))
			return False
		maxSteps=5 #changing this changes the depth of recursion, and slows the game.
		for limit in range(1,maxSteps):
			if solve(Warrior.x, Warrior.y, limit):
				return visited 
			else: visited=[] #reset just in case.

	@staticmethod
	def solveMaze(Warrior,data):
		increment=Warrior.radius*2
		solutionList=MazeSolver.solveMazeHelper(Warrior, data)
		if solutionList==None:
			return
		finalDest=Warrior.destinations[0]
		solutionList.append(finalDest)
		Warrior.destinations=solutionList

