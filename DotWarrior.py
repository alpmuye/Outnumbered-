from tkinter import *
import math
import random
from Bullet import *
from MazeSolver import *
from Strategy import *
from helperFunctions import *

#different classes of DotWarriors. Red and Blue. Smart and Dumb.

#################################################################################
class DotWarrior(object):
	
	startingAngle= math.pi
	radius=10 #for outside class access.

	def __init__(self, x, y):
		(self.x, self.y)=(x,y)
		self.radius=DotWarrior.radius
		self.velocity=2
		self.vx=0
		self.vy=0
		self.angularSpeed=math.pi/100
		self.angle=DotWarrior.startingAngle
		self.headAngle=self.angle
		self.isSelected=False
		self.destinations=[] 
		self.isStop=False
		self.healthPoints=100
		self.stopCount=0
		self.fireDelay=0 
		self.shootingRange=70
		self.isInSquad=False

	def __repr__(self): #for debugging purposes.
		return "<Warrior at (%s, %s)>" % (self.x, self.y)


	###############################################
		########## Some AI Helpers  ###########
	###############################################

	#imported from Find_ClosestEnemy Attack AI.
	def findEnemyToAttack(self, data): #returns x,y of the closest enemy in range.
		closestDistance=None		   #and not if in fog of war!!
		enemyToAttack=None
		myCoordinates=(self.x, self.y)
		for Warrior in data.Warriors:
			if isThereObstacleInSight(data, self, Warrior): continue 
			if Warrior.type!=self.type:							
				enemyCoordinates=(Warrior.x, Warrior.y)
				thisDistance=getDistance(myCoordinates, enemyCoordinates)
				if closestDistance==None or thisDistance<closestDistance:
					closestDistance=thisDistance 
					enemyToAttack=Warrior
		return enemyToAttack

	def getGroupStrength(self, group):
		strength=0
		for Warrior in group:
			strength+=Warrior.healthPoints
		return strength 

	def getNearbyAllies(self, data):
		locRange=self.shootingRange*2
		myLoc=(self.x, self.y)
		nearbyAllies=[]
		for Warrior in data.Warriors:
			if type(Warrior)==type(self):
				distance=getDistance(myLoc, (Warrior.x, Warrior.y))
				if distance<=locRange: nearbyAllies.append(Warrior)
		return nearbyAllies 

	def getNearbyEnemies(self, data):
		locRange=self.shootingRange*2
		myLoc=(self.x, self.y)
		nearbyEnemies=[]
		for Warrior in data.Warriors:
			if type(Warrior)!=type(self):
				distance=getDistance(myLoc, (Warrior.x, Warrior.y))
				if distance<=locRange: nearbyEnemies.append(Warrior)
		return nearbyEnemies

	def isBeingOverPowered(self, data):
		minHP=7
		maxHP=100
		if self.healthPoints<minHP: return True
		if self.healthPoints>=maxHP: return False
		overPowerRatio=1.7 #if outPowered by this ratio, better run.
						   #ratio result of diligent gameplay experimentation.
		nearbyAllies=self.getNearbyAllies(data)
		nearbyEnemies=self.getNearbyEnemies(data)
		if (self.getGroupStrength(nearbyEnemies)/self.getGroupStrength(nearbyAllies)
								>=overPowerRatio):
			return True 
		else:
			return False

	def isRetreatOver(self, data):
		retreatDist=200
		EnemyLocations=[]
		for enemy in data.Warriors:
			if type(enemy)==type(self): continue
			EnemyLocations.append((enemy.x, enemy.y))
		enemiesCOF=getCenterPoint(*EnemyLocations)
		distance=getDistance((self.x, self.y), enemiesCOF)

		return distance>retreatDist
			
	###############################################
	########## Aesthetics are Important ###########
	###############################################

	def changeColor(self): #color symbolizing health points.
		maxHealthPoints=100
		colorIntensity=self.healthPoints/maxHealthPoints
		maxColorGradient=255

		if not self.R==0: self.R=round(maxColorGradient*colorIntensity)
		if not self.G==0: self.G=round(maxColorGradient*colorIntensity)
		if not self.B==0: self.B=round(maxColorGradient*colorIntensity)

		self.fill=rgbString(self.R, self.G, self.B)

	#######################################
	########## Movement Methods ###########
	#######################################

	def getVelocityVectors(self): #adjusts velocity components according to dest
		if self.destinations==[]: return #(None, None)]: return 
		currentCoordinates=(self.x, self.y)
		(destX, destY)=self.destinations[0] #go towards the first one.
		(deltaX, deltaY)= (destX-self.x, destY-self.y)
		self.angle=getAngleFromDeltas(deltaX, deltaY)
		(vx, vy)=balanceVelocityIntoVectors(self.velocity, self.angle)
		(self.vx, self.vy)=(vx,vy)

	def doesIntersectWithObstacles(self, data):
		WarriorCenter=(self.x, self.y)
		WarriorRadius=self.radius 
		for item in data.Map.items:
			if doesPointIntersectWithItem(WarriorCenter, WarriorRadius, item):
				if item.isMovable:
					dx=self.vx*item.slowDownFactor
					dy=self.vy*item.slowDownFactor
					self.x-=dx
					self.y-=dy
					return False 
				return True
		return False

	def move(self, data): #trial and error. Too many errors (3)
		self.x+=self.vx	  #triggers the maze solver algorithm to resolve
		self.y+=self.vy   #movement conflicts.
		if self.doesIntersectOtherSoldier(data):
			self.takeStepBack()
			return
		elif self.isOutOfBounds(data):
			self.stopCount-=1 #map exits should not trigger maze solver.
			self.takeStepBack()
			return
		elif self.doesIntersectWithObstacles(data):
			self.takeStepBack()
			return
		else:
			self.stopCount=0

	def takeStepBack(self): #if not legal move.
		self.x-=self.vx
		self.y-=self.vy
		self.stopCount+=1

	def setDestination(self, x, y): #through mouseClick
		self.destinations=[(x, y)]
		self.getVelocityVectors()

	def appendDestination(self, x, y): #for queue movement
		self.destinations.append((x, y))
		if len(self.destinations)==1: #append was the first move.
			self.getVelocityVectors() #so get moving now.

	def checkForDestinationArrival(self):
		if not self.destinations==[]:
			if closeEnough((self.x, self.y), self.destinations[0]):
				self.destinations.pop(0) #this destination reached.
				self.getVelocityVectors()
		else:
			(self.vx, self.vy)=(0,0) #if reached destination, stop

	def rotateHead(self):  
		rotateRatio=20 #the rotation speed at 20 just feels right.
		delta=self.angle-self.headAngle
		epsilon=0.05 #close enuff.
		if not abs(delta)<=epsilon:
			self.headAngle+=delta/rotateRatio

	######################################
	########## Legality Checking #########
	######################################

	def doesIntersectOtherSoldier(self, data): #DATA needed for group movement
		for otherWarrior in data.Warriors:
			if otherWarrior==self: continue # "that's me yo."
			point1=(self.x, self.y)	#as in don't intersect with yourself.
			point2=(otherWarrior.x, otherWarrior.y)
			distance=getDistance((point1), (point2))
			if (self.radius+otherWarrior.radius)>=distance:
				return True
		return False

	def isOutOfBounds(self, data):
		if self.x+self.radius>=data.width or self.y+self.radius>=data.height:
			return True
		if self.x-self.radius<=0 or self.y-self.radius<=0:
			return True 
		return False

	def contains(self, x, y): #for Mouse clicks
		distance= getDistance((self.x, self.y), (x,y))
		return distance<=self.radius


	####################################
	#######  The Update Method #########
	####################################

	def regenerate(self):
		maxHealthPoints=100
		if not self.healthPoints>=maxHealthPoints:
			self.healthPoints+=0.1

	def handleFireDelay(self):
		if not self.fireDelay==0: self.fireDelay-=1
	
	def handleMovementConflicts(self, data):
		maxStopCount=10 #if had to take step back 10 times in a row;
						#pretty much means that the troop is stuck.
		if self.stopCount>=maxStopCount:
			if len(self.destinations)==0: return 
			self.destinations.pop(0)
			self.stopCount=0 #so cancel movement.

						#maze solver triggering happens in classes. not here.

	def update(self, data): #data is the animation "self".
		self.handleFireDelay()
		self.handleMovementConflicts(data)
		self.changeColor()
		self.regenerate()	
		self.move(data)
		self.rotateHead()

	###############################
	#######  Draw Methods #########
	###############################

	def drawSelection(self, canvas):
		(cx, cy, smallR)=(self.x, self.y, self.radius/2)
		canvas.create_oval(cx-smallR,cy-smallR,
				cx+smallR, cy+smallR, fill="light blue", width=1,
				tags="delete")

	def drawHead(self, canvas):
		r=self.radius
		headX=self.x +  r*math.cos(self.headAngle)
		headY=self.y +   r*math.sin(self.headAngle)
		canvas.create_line((self.x, self.y), (headX, headY), fill="black", 
			width=2, tags="delete")
		
	def drawSquadIndicator(self, canvas, data):
		(cx, cy)=(self.x, self.y)
		r=2
		#draw Squad indicator.
		if self.isInSquad: 
			for squad in data.Squads:
				if self in squad.Warriors:
					canvas.create_oval(cx-r, cy-r, cx+r, cy+r,
											fill=squad.color, tags="delete")

	def draw(self, canvas, data):
		(cx, cy, r)=(self.x, self.y, self.radius)
		try:
			canvas.create_oval(cx-r,cy-r,cx+r, cy+r, fill=self.fill, 
				tags="delete")
		except: #for random RGB string errors.
			self.fill="red" if type(self)==Red else "blue"
			canvas.create_oval(cx-r,cy-r,cx+r, cy+r, fill=self.fill,
				tags="delete")

		if self.isSelected: self.drawSelection(canvas)
		if self.isInSquad: self.drawSquadIndicator(canvas, data)
		self.drawHead(canvas)


############################################################################
############################################################################
############################################################################
########################## Computer Classes ################################
############################################################################
############################################################################
############################################################################
"""
AI classes do not inherit from each other so that the super() in the 
update method stays intact. However, they mostly have identical inits.

"""
class Red(DotWarrior):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.type="enemy" #for outside access without imports and inheritance.
		(self.R, self.G, self.B)= (255, 0, 0) #RED
		self.fill=rgbString(self.R, self.G, self.B)
		self.angle= math.pi/2 #start looking down.
		self.AI=None
		self.exploreTimer=0 #to fix the AI to explore mode.

	def setDestination(self, x, y): pass #So that you don't control the AI.

#the AI class gets 
#reconstructed and updated
#at each timerFired.

	def getAI_state(self, data):
		maxExploreTimer=50
		if self.findEnemyToAttack(data)==None: #no enemy in sight. then explore.
			self.AI=Explore(self, data)
			self.exploreTimer=maxExploreTimer
		else: self.AI=FindClosestEnemy_Attack(self, data) #engage.

	def update(self, data):
		if not self.exploreTimer<=0: 
			self.exploreTimer-=1
			super().update(data)
			return
		self.getAI_state(data)
		self.AI.behave()
		super().update(data)
############################################################################

class TutorialRed(DotWarrior): #Immobile enemy for tutorial purposes.
	def __init__(self, x, y):
		super().__init__(x, y)
		self.type="enemy"
		(self.R, self.G, self.B)= (255, 0, 0) #RED
		self.fill=rgbString(self.R, self.G, self.B)

	def setDestination(self, x, y): pass #So that you don't control the AI.


############################################################################
############################################################################

class InvaderRed(DotWarrior): #AI that specializes on capturing 
								#outposts unless threatened. 

	def __init__(self, x, y):
		super().__init__(x, y)
		self.type="enemy"
		(self.R, self.G, self.B)= (255, 0, 0) 
		self.fill=rgbString(self.R, self.G, self.B)
		self.angle= math.pi/2 
		self.AI=None
		self.exploreTimer=0 #to fix the AI to explore mode.
		self.foundOutpost=False

	def findOutpostToCapture(self, data):
		closestDistance=None
		outpostToCapture=None
		myLoc=(self.x, self.y)
		for outpost in data.Outposts:
			if isThereObstacleInSight(data, self, outpost): continue
			if outpost.Occupier=="red": continue #it's already under control.
			outPostLoc=(outpost.x, outpost.y)
			distance=getDistance(myLoc, outPostLoc)
			if closestDistance==None or distance<closestDistance:
				closestDistance=distance 
				outpostToCapture=outPostLoc
		return outpostToCapture

	def getAI_state(self, data):
		maxHealthPoints=100
		hitFactor=0.9
		maxExploreTimer=50
		if self.healthPoints<maxHealthPoints*0.9: #only defend if you've been 
												   #hit seriously.
			self.AI=FindClosestEnemy_Attack(self, data)
			return
		self.dest=self.findOutpostToCapture(data) #store it for efficiency.
		if self.dest==None:					#you don't have to call it below.
			self.AI=Explore(self, data)
			self.exploreTimer=maxExploreTimer
			return

	def update(self, data):
		self.AI=None
		if not self.exploreTimer<=0:
			self.exploreTimer-=1
			super().update(data)
			return
		self.getAI_state(data)
		#The outpost capturing AI, is a part of the update function.
		if self.AI==None:				#i.e not a separate class.
			outpostRange=70 #somewhere within the outpost.
			self.destinations=[self.dest]
			if getDistance((self.x, self.y), self.destinations[0])>outpostRange:
				#this way, invader does not stay put, and may avoid enemy fire.
				self.getVelocityVectors()
			super().update(data)
			return
		self.AI.behave()
		super().update(data)

############################################################################
############################################################################

class SmarterRed(DotWarrior):	#smarterRed allocates enemies amongst the
	def __init__(self, x, y):	#ranks, instead of acting individually.
		super().__init__(x, y)	#means better coordination!
		self.type="enemy"
		(self.R, self.G, self.B)= (255, 0, 0) #RED
		self.fill=rgbString(self.R, self.G, self.B)
		self.angle= math.pi/2 #start looking down.
		self.AI=None
		self.exploreTimer=0 #to fix the AI to explore mode.
		self.retreatTimer=0

	def setDestination(self, x, y): pass #Don't control the AI!!!

	def isInFiringRangeOfDesignatedEnemy(self):
		myLoc=(self.x, self.y)
		enemyLoc=(self.destinations[0])
		firingRange=70
		if getDistance(myLoc, enemyLoc)<firingRange:
			return True
		else:
			return False

	def getAI_state(self, data):
		if self.retreatTimer!=0: #stay in retreat mode for a duration.
			self.AI=basicRetreat(self, data)
			return
		#so that doesn't get stuck between attacking and retreating. 
		shareEnemies(self, data).behave() #this sets destination.
		if self.destinations==[]: #Victorious.
			self.AI=shareEnemies(self, data)
			return
		if self.isInFiringRangeOfDesignatedEnemy():
			self.AI=FindClosestEnemy_Attack(self, data)
		else:
			self.AI=shareEnemies(self, data) 
			#keep on using the smart algorithm until within range of enemy.
		if self.isBeingOverPowered(data):
			self.AI=basicRetreat(self, data)
			self.retreatTimer=70 #retreat for 70 steps before changing mind, 
								 #prevents getting stuck in the attack/retreat
								 #limbo.

	def update(self, data):
		if not self.retreatTimer<=0: #just follow through the retreat process
			self.retreatTimer-=1     #until within a reasonable distance.
			super().update(data)
			return
		self.getAI_state(data)
		self.AI.behave()
		super().update(data)

############################################################################
############################################################################

class SmartestRed(DotWarrior):	#smartestRed allocates the enemy, as well
								#as the attacking position to most 
	def __init__(self, x, y):	#efficiently surround the enemy.
		super().__init__(x, y)	#Strongest AI Class!!
		self.type="enemy"
		(self.R, self.G, self.B)= (255, 0, 0) #RED
		self.fill=rgbString(self.R, self.G, self.B)
		self.angle= math.pi/2 #start looking down.
		self.AI=None
		self.isSolvingMaze=False
		self.retreatTimer=0

	def getAI_state(self, data): #same structure as smart Red.
		if self.retreatTimer!=0: #Different AI class.
			self.AI=basicRetreat(self, data)
			return 
		surroundEnemies(self, data).behave() 
		if self.destinations==[]: #Victorious.
			self.AI=FindClosestEnemy_Attack(self, data)
			return
		if self.isInPosition(): 
			self.AI=FindClosestEnemy_Attack(self, data)
		else:
			self.AI=surroundEnemies(self, data) 
			#keep on using the smart algorithm until within range of enemy.
		if self.isBeingOverPowered(data):
			self.AI=advancedRetreat(self, data)
			self.retreatTimer=70

	def handleMovementConflicts(self, data):
		maxStopCount=10 #if had to take step back 10 times in a row;
						#pretty much means that the troop is stuck.
		if self.destinations==[]: return
		if self.stopCount>=maxStopCount:
			MazeSolver.solveMaze(self, data)
			self.isSolvingMaze=True
			self.stopCount=0

	def setDestination(self, x, y): pass 

	def isInPosition(self):
		myLoc=(self.x, self.y)
		target=self.destinations[0]
		radius=50 #if within 3 pixels of designated position, youre good.
		distance=getDistance(myLoc, target)
		return (distance<=radius)

	def update(self, data):
		if self.isSolvingMaze:
			self.checkForDestinationArrival()
			if len(self.destinations)<2: self.isSolvingMaze=False
			#fixes the bug when destination is unreachable, i.e. in an item.
		if not self.retreatTimer<=0: #just follow through the retreat process
			self.retreatTimer-=1     #until within a reasonable distance.
			super().update(data)
			return
		if not self.isSolvingMaze:
			self.getAI_state(data) 
			self.AI.behave()
		super().update(data)

############################################################################
############################ Player Class ##################################
############################################################################	

class Blue(DotWarrior): #this is you
	def __init__(self, x, y):
		super().__init__(x, y)
		(self.R, self.G, self.B)= (0, 0, 255) #BLUE
		self.fill=rgbString(self.R, self.G, self.B)
		self.angle= 3*math.pi/2 #start looking up.
		self.mode="movement"
		self.type="player"

	########################################################################
	######################### Attack Mode Methods ##########################
	########################################################################

	def checkIfClearShot(self, data, Enemy): 
		enemyLoc=(Enemy.x, Enemy.y)
		myLoc=(self.x, self.y)
		testPoints=getClearShotTestPoints(myLoc, enemyLoc)
		for Warrior in data.Warriors:
			if type(Warrior)==type(self) and Warrior!=self: #all the allies
														#and not self.
				for testPoint in testPoints:
					(x,y)=testPoint
					if Warrior.contains(x, y): #whoops. hold fire.
						return False
		return True

	def fire(self, data):
		data.bullets.append(Bullet(self.x, self.y, self.headAngle, self))

	def isThereNearbyEnemy(self, data):
		shootingRangeFactor=1.5
		shootingRange=self.shootingRange*shootingRangeFactor
		myLoc=(self.x, self.y)
		for Warrior in data.Warriors:
			if type(Warrior)!=type(self):
				enemyLoc=(Warrior.x, Warrior.y)
				distanceToEnemy=getDistance(myLoc, enemyLoc)
				if distanceToEnemy<=shootingRange:
					return True
		return False

	def getEnemy(self, data):
		if not len(self.destinations)==1: assert(False) #should only have a 
											#single dest by this point.
											# i.e. the Enemy Warrior.
		dest=self.destinations[0]
		(x, y)=dest
		for Warrior in data.Warriors:
			if Warrior.contains(x, y):
				return Warrior
		return self.findEnemyToAttack(data)
		#enemy moved as the soldier was attempting to engage.


	def attackTargetEnemyIfInRange(self, data): #does the actual firing.
		shootingRange=self.shootingRange
		Enemy=self.getEnemy(data)
		myCoordinates=(self.x, self.y)
		enemyCoordinates=(Enemy.x, Enemy.y)
		distanceToEnemy=getDistance(myCoordinates, enemyCoordinates)
		if distanceToEnemy<shootingRange:
			(self.vx, self.vy)=(0, 0) #stop and shoot.
			if self.checkIfClearShot(data, Enemy):
				if self.fireDelay==0:
					self.fire(data)
					self.fireDelay=50 #back to start.

	########################################################################
	########################################################################

	def isAttackOrdered(self, data):
		for dest in reversed(self.destinations):
			(x,y)=dest
			for Warrior in data.Warriors:
				if Warrior.contains(x,y) and type(Warrior)!=type(self):
					self.destinations=[(x, y)] #override everything and attack.
					#self.isSelected=False
					return True 
		#if it gets here, either attack never ordered, or enemy killed.
		return False
	
	def isMovementOrdered(self, data):
		for dest in self.destinations:
			(x,y)=dest
			for Warrior in data.Warriors:
				if Warrior.contains(x,y) and type(Warrior)!=type(self):
					return False #one of the destinations is attacking. 
		if not self.destinations==[]: return True
		else: return False
	
	def getMode(self, data):
		#manual control here.
		if self.mode=="defend" and not self.isThereNearbyEnemy(data):
			self.mode="movement" #exit from AI to implement fog of war.
		if not self.mode=="defend" or self.isSelected:
			if self.isAttackOrdered(data):
				self.mode="attack"
			if self.isMovementOrdered(data):
				self.mode="movement" #movement overrides attack
		#auto-pilot down below.
		if (not self.isMovementOrdered(data) and 
									not self.isAttackOrdered(data)
						and not self.isSelected):
			if self.isThereNearbyEnemy(data):
				self.mode="defend"
			else:
				self.mode="movement"

	def handleMovementConflicts(self, data):
		maxStopCount=3 
		if self.stopCount>=maxStopCount:
			MazeSolver.solveMaze(self, data)
			self.stopCount=0

	def update(self, data):
		self.getMode(data)
		if self.mode=="movement":
			self.checkForDestinationArrival()
		elif self.mode=="attack":
			self.attackTargetEnemyIfInRange(data)
		elif self.mode=="defend": #defend position using the enemy AI.
			defendingAI=FindClosestEnemy_Attack(self, data)
			defendingAI.behave()
		super().update(data)
