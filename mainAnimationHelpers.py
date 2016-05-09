
from DotWarrior import *
from Animation import *
from Bullet import *
from helperFunctions import *
from Squad import *
from MapItems import *

#####################################################
			# < Key Pressed Helpers >

def clearSelections(self):
	for Warrior in self.Warriors:
		Warrior.isSelected=False
		Warrior.mode="defend"
		if Warrior.isInSquad:
			for squad in self.Squads:
				if Warrior in squad.Warriors:
					squad.isSelected=False

def handleSquadRotations(self, event):
	for squad in self.Squads:
		if squad.isSelected:
			if event.keysym=="Left":
				squad.rotateLeft()
			else: #event.keysym=="Right"
				squad.rotateRight()

def breakSquad(self, Warrior):
	for squad in self.Squads:
		if Warrior in squad.Warriors: #found squad to break
			for Warrior in squad.Warriors:
				Warrior.isInSquad=False
			self.Squads.remove(squad)
			break 

def handleSquadBindings(self):
	warriorsInSquad=[]
	for Warrior in self.Warriors:
		if Warrior.isSelected:
			if Warrior.isInSquad: 
				breakSquad(self, Warrior)
				warriorsInSquad=[]
				break 
			warriorsInSquad.append(Warrior)
			Warrior.isInSquad=True
	if warriorsInSquad!=[]:
		self.Squads.append(Squad(warriorsInSquad))


			# < / Key Pressed Helpers >
#####################################################


#####################################################
			# < Mouse Event Helpers >

def handleWarriorSelects(self, x, y):
	for Warrior in self.Warriors:
		if Warrior.isInSquad: continue
		if Warrior.contains(x, y) and type(Warrior)==Blue: 
			Warrior.isSelected=not Warrior.isSelected
			return True
	return False   #return values show whether selections were made 

def appendWarriorDestination(self, x ,y):
	for Warrior in self.Warriors:
		if Warrior.isInSquad: continue
		if Warrior.isSelected:
			Warrior.appendDestination(x, y)

def handleWarriorDestinations(self, x ,y):
	didHandle=False
	n=len(getSelectedWarriors(self))
	for Warrior in self.Warriors:
		if Warrior.isInSquad: continue
		if Warrior.isSelected: 
			Warrior.setDestination(x, y)
			didHandle=True
			if n==1:
				Warrior.isSelected=False 
				return #don't stay selected for single unit movements!
					   #recommendation of roommate, to make combat less
					   #frustrating!
	return True if didHandle else False 

def handleRectangleSelects(self):
	x0,y0=self.mouseMovements[0]  #first one
	x1,y1=self.mouseMovements[-1] #last one
	recBounds=(x0,y0,x1,y1)
	for Warrior in self.Warriors:
		if Warrior.isInSquad or type(Warrior)!=Blue: continue 
		WarriorCenter=(Warrior.x, Warrior.y)
		if isDotInBounds(recBounds, WarriorCenter):
			Warrior.isSelected=True

def getSelectedWarriors(self):
	listOfSelectedWarriors=[]
	for Warrior in self.Warriors:
		if Warrior.isSelected: 
			listOfSelectedWarriors.append(Warrior)
	return listOfSelectedWarriors

def handleSquadSelects(self, x, y):
	for squad in self.Squads:
		if squad.contains(x, y):
			squad.isSelected=not squad.isSelected
			return True
	return False

def handleSquadDestinations(self, x, y):
	for squad in self.Squads:
		if squad.isSelected:
			squad.changeCenterOfMass(x, y) #and change the angles too.
			for warrior in squad.Warriors:
				(distance, angle)=squad.WarriorLocDict[warrior]
				(dx,dy)=balanceVelocityIntoVectors(distance,angle)
				warrior.setDestination(x-dx, y-dy)

def getDestinationsFromFormationCoordinates(self):
	#helper for selected HandleWarriorFormation
	#returns the list of destinations given mouseEvents and
	#number of selected troops.
	listOfSelectedWarriors=getSelectedWarriors(self) 
	amountOfSelectedWarriors=len(listOfSelectedWarriors)
	lenOfCoordinates=len(self.formationCoordinates)
	indexIncrement=round(lenOfCoordinates/amountOfSelectedWarriors)
	if indexIncrement==0: return
	listOfDestinations=[]
	for index in range(0, lenOfCoordinates, indexIncrement):
		try:
			positions=self.formationCoordinates[index:index+indexIncrement]
			destToAdd=getCenterPoint(*positions)
			listOfDestinations.append(destToAdd)
		except: #for unexpected list bugs.
			break
	return listOfDestinations

def handleSelectedWarriorFormation(self):
	listOfSelectedWarriors=getSelectedWarriors(self) 
	listOfDestinations=getDestinationsFromFormationCoordinates(self)
	if listOfDestinations in [[], None]: return
	for destination in listOfDestinations:
		distance=None
		closestWarrior=None
		for Warrior in listOfSelectedWarriors: #pick the closest.
			thisDistance=getDistance((Warrior.x, Warrior.y), destination)
			if distance==None or thisDistance<distance:
				distance=thisDistance
				closestWarrior=Warrior 
		(destX, destY)=destination
		closestWarrior.setDestination(destX, destY)
		listOfSelectedWarriors.remove(closestWarrior)
		if len(listOfSelectedWarriors)==0: return


			# < / Mouse Event Helpers >
#####################################################


#####################################################
			# < Timer Fired  Helpers >

def removeDeadSoldierFromSquad(self, Warrior):
	for squad in self.Squads:
		if Warrior in squad.Warriors:
			 squad.Warriors.remove(Warrior)

def updateWarriors(self):
	for Warrior in self.Warriors:
		if Warrior.healthPoints<=0:
			if Warrior.isInSquad: removeDeadSoldierFromSquad(self, Warrior)
			self.Warriors.remove(Warrior) #R.I.P.
		else:
			Warrior.update(self) 

def updateSquads(self):
	for squad in self.Squads:
		if len(squad.Warriors)==0:
			self.Squads.remove(squad)
		squad.update()

def updateBullets(self):
	for bullet in self.bullets:
		bullet.update(self)
		if bullet.lifeTime>=self.bulletMaxLifeTime:
			self.explosions.append(Explosion(bullet.x, bullet.y)) 
			self.bullets.remove(bullet)

def updateOutposts(self):
	for outpost in self.Outposts:
		outpost.update(self)

def updateExplosions(self):
	maxExplosionSize=4
	for explosion in self.explosions:
		if explosion.radius>=maxExplosionSize:
			self.explosions.remove(explosion)
		else:
			explosion.update()

			# < / Timer Fired Helpers >
#####################################################


#####################################################
			# < redrawAll  Helpers >

def drawMap(self, canvas):
	canvas.create_rectangle(0,0, self.width, self.height, width=0,
		fill="light green")
	for item in self.Map.items:
		item.draw(canvas)

########						########
########   Fog Of War Function  ########
########						########


def isThereObstacleInSight(self, BlueWarrior, Warrior):
	deltaX=Warrior.x-BlueWarrior.x
	deltaY=Warrior.y-BlueWarrior.y 
	angle=getAngleFromDeltas(deltaX, deltaY)
	step=2
	(incrementX, incrementY)=balanceVelocityIntoVectors(step, angle)
	(testPointX, testPointY)=(BlueWarrior.x+incrementX,
								 BlueWarrior.y+incrementY)
	while not Warrior.contains(testPointX,testPointY):
		for item in self.Map.items:
			if item.isTransparent: continue
			if item.contains(testPointX, testPointY):
				return True
		testPointX+=incrementX
		testPointY+=incrementY
	return False #direct connection to enemy Warrior.

def isWarriorInFogOfWar(self, Warrior): #for drawing purposes.
	if type(Warrior)==Blue: return False 
	maximumSight=500
	for BlueWarrior in self.Warriors:
		if not type(BlueWarrior)==Blue: continue
		distanceToEnemy=getDistance((BlueWarrior.x, BlueWarrior.y),
								(Warrior.x, Warrior.y))
		if distanceToEnemy<maximumSight:
			if not isThereObstacleInSight(self, BlueWarrior, Warrior):
				return False
	return True

def drawWarriors(self, canvas):
	for Warrior in self.Warriors:
		if self.fogOfWarActive:
			if isWarriorInFogOfWar(self, Warrior): continue
		Warrior.draw(canvas, self) 
		
def drawBullets(self, canvas):
	for bullet in self.bullets:
		bullet.draw(canvas)

def drawSelectionRectangle(self, canvas):
	topLeft=self.mouseMovements[0]
	bottomRight=self.mouseMovements[-1]
	canvas.create_rectangle(topLeft, bottomRight, tags="delete")

def drawOutposts(self, canvas):
	for outpost in self.Outposts:
		outpost.draw(canvas)

def drawExplosions(self, canvas):
	for explosion in self.explosions:
		explosion.draw(canvas)

def drawLineFromFormationCoordinates(self, canvas):
	for i in range(len(self.formationCoordinates)-1): #not inclusive.
		startCoordinate=self.formationCoordinates[i]
		endCoordinate=self.formationCoordinates[i+1]
		canvas.create_line(startCoordinate, endCoordinate, width=5, 
			tags="delete")

			# < / redrawAll Helpers >
#####################################################
