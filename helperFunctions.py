
import math
import random

#useful helper functions used at different classes.

def tossCoin(): #such complexity, much randomness.
	booleans=[True, False]
	return random.choice(booleans)

def rgbString(red, green, blue): #Courtesy of Class Notes.
    return "#%02x%02x%02x" % (red, green, blue)

def getAngleFromDeltas(deltaX, deltaY):
	try:
		slope=deltaY/deltaX
		angle= math.atan(slope)
		if deltaX<0: angle+=math.pi #this fixes the quadrants 1&2
	except: #deltaX=0, either looking up or directly down.
		angle=math.pi/2 if deltaY>0 else -math.pi/2
	return angle 


def isDotInBounds(bounds, dot): #for rectangle selects
	(x0,y0,x1,y1)=bounds 
	(x, y)=dot
	return (((x0<=x<=x1) and (y0<=y<=y1)) or ((x1<=x<=x0) and
		(y1<=y<=y0)) or ((x0<=x<=x1) and (y1<=y<=y0)) or 
				(x1<=x<=x0)	and (y0<=y<=y1)) 

def balanceVelocityIntoVectors(velocityComponent, angle):
	#this distributes your total velocity vectors in the X and Y dirs.
	vx= velocityComponent * math.cos(angle)
	vy= velocityComponent * math.sin(angle)
	return (vx, vy)

def getDistance(point1, point2): #gets the distance between two points
								 #represented by tuples.
	(x0, y0)= point1
	(x1, y1)= point2
	return ((x1-x0)**2 + (y1-y0)**2)**0.5

def closeEnough(point1, point2): #prevents exactness bugs
								#in reaching destination
	epsilon=3 #if you are 3 pixels near the destination, you are good
	distanceBetweenPoints=getDistance(point1, point2)
	return distanceBetweenPoints<=epsilon

def closeEnoughMaze(point1, point2):
	epsilon=10 #if you are 10 pixels near the destination, you are good
	distanceBetweenPoints=getDistance(point1, point2)
	return distanceBetweenPoints<=epsilon

def getMiddlePoint(point1, point2): #for the recursive is clearShot function.
	(x0, y0)= point1
	(x1, y1)= point2
	xMid=round((x0+x1)/2)
	yMid=round((y0+y1)/2)
	return (xMid, yMid)

def getCenterPoint(*args): #to get the middle point of multiple points.
	(totalX, totalY)=(0,0) #i.e center of mass, since all masses are equal.
	totalPoints=len(args)
	for point in args:
		totalX+=point[0]
		totalY+=point[1]
	return (totalX/totalPoints, totalY/totalPoints)

def getClearShotTestPoints(myLoc, enemyLoc):
#This returns test points in a line, to prevent friendly fire.
		maxSteps=4
		if getDistance(myLoc, enemyLoc)<=10:
			#an ally cannot fit in this area anymore
			return []
		else: #recursion.
			pointsToCheck=[]
			middlePoint=getMiddlePoint(myLoc, enemyLoc)
			pointsToCheck.append(middlePoint)
			pointsOnTheLeft= getClearShotTestPoints(myLoc, middlePoint)
			pointsOnTheRight= getClearShotTestPoints(middlePoint, enemyLoc)
			return (pointsToCheck)+(pointsOnTheLeft)+(pointsOnTheRight)

##############################################################################
##############################################################################

def doesPointIntersectWithItem(WarriorCenter, WarriorRadius, item): 
	itemCenter=(item.x, item.y)
	distance=getDistance(WarriorCenter, itemCenter)
	minDistance=(item.radius + WarriorRadius)
	return True if distance<=minDistance else False
