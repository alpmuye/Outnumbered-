
from Bullet import *
from helperFunctions import *
from MazeSolver import *
import copy

########################################################################
########################################################################
####################### Strategy (AI) Class ############################
########################################################################
########################################################################

class Strategy(object):

	def __init__(self, WarriorClass, GameClass):
		self.WarriorClass=WarriorClass #this may be referred to as Tim later on.
		self.GameClass=GameClass #this may be referred to as Game.
		self.shootingRange=70
		self.isRetreating=False

	def isOutOfBounds(self, x, y):
		Tim=self.WarriorClass
		Game=self.GameClass
		if x+Tim.radius>=Game.width or y+Tim.radius>=Game.height:
			return True
		if x-Tim.radius<=0 or y-Tim.radius<=0:
			return True 
		return False

	def fire(self):
		Game=self.GameClass
		Tim=self.WarriorClass #Tim is a brave warrior.
		Game.bullets.append(Bullet(Tim.x, Tim.y, Tim.headAngle, Tim))

	def checkIfClearShot(self, closestEnemy): #is Ally in the way?
		Tim=self.WarriorClass #Tim has a really short name.
		enemyLoc=(closestEnemy.x, closestEnemy.y)
		myLoc=(Tim.x, Tim.y)
		testPoints=getClearShotTestPoints(myLoc, enemyLoc)
		for Warrior in self.GameClass.Warriors:
			if type(Warrior)==type(Tim) and Warrior!=Tim: #all the allies
														  #and not self.
				for testPoint in testPoints:
					(x,y)=testPoint
					if Warrior.contains(x, y): #whoops. hold fire.
						return False
		return True

	def behave(self): pass #main framework.


########################################################################
########################################################################
 ################### Retreat & Exploration ############################
########################################################################
########################################################################

class basicRetreat(Strategy):
		#for smarterRed, only runs away from nearby enemy COF
	def behave(self):
		self.initiateRetreat()

	def initiateRetreat(self):
		self.RetreatAwayFromEnemyCOF()

	def getNearbyEnemies(self):
		Game=self.GameClass
		Tim=self.WarriorClass
		locRange=self.shootingRange*2
		myLoc=(Tim.x, Tim.y)
		nearbyEnemies=[]
		for Warrior in Game.Warriors:
			if type(Warrior)!=type(Tim):
				distance=getDistance(myLoc, (Warrior.x, Warrior.y))
				if distance<=locRange: nearbyEnemies.append(Warrior)
		return nearbyEnemies

	def isLegalEscapePoint(self, x, y):
		Game=self.GameClass
		if self.isOutOfBounds(x, y): return False 
		for item in Game.Map.items:
			if item.contains(x, y):
				return False
		return True  

	def getEscapePoints(self, angle):
		Tim=self.WarriorClass
		Game=self.GameClass
		step=100 #distance that will be travelled.
		potentialAngle=angle 
		increment=math.pi/4
		incrementCount=0
		while True:
			if incrementCount>=9: #tried each way, didn't work
				return []
			(vectorX, vectorY)=balanceVelocityIntoVectors(step, potentialAngle)
			(destX,destY)=(Tim.x+vectorX, Tim.y+vectorY)
			if self.isLegalEscapePoint(destX, destY):
				return [(destX, destY)]
			else:
				potentialAngle+=increment
				incrementCount+=1

	def RetreatAwayFromEnemyCOF(self):
		Tim=self.WarriorClass
		nearbyEnemyLocations=[]
		distanceCheck=getDistance((Tim.x, Tim.y), Tim.destinations[0]) 
		for enemy in self.getNearbyEnemies():
		#get the enemy COF from nearby enemy locations.
			nearbyEnemyLocations.append((enemy.x, enemy.y))
		enemiesCOF=getCenterPoint(*nearbyEnemyLocations)
		(enemyX, enemyY)=enemiesCOF
		(deltaX, deltaY)=(Tim.x-enemyX, Tim.y-enemyY)
		angle=getAngleFromDeltas(deltaX, deltaY)
		Tim.destinations=self.getEscapePoints(angle)
		Tim.getVelocityVectors()


#used for SmarterRed retreat. Retreats near an enemy 
#that is not being overpowered.
class advancedRetreat(basicRetreat):
	def getAlly(self):
		Game=self.GameClass
		Tim=self.WarriorClass
		closestSoFar=None
		closestDistance=None
		for Warrior in Game.Warriors:
			if not type(Tim)==type(Warrior): continue
			if Warrior.isBeingOverPowered(Game): continue
			distance=getDistance((Tim.x, Tim.y), (Warrior.x, Warrior.y))
			if closestDistance==None or distance<closestDistance:
				closestDistance=distance
				closestSoFar=Warrior 
		return closestSoFar

	def moveTowardsAlly(self, ally):
		Game=self.GameClass
		Tim=self.WarriorClass

		Tim.destinations=[(ally.x, ally.y)]
		Tim.getVelocityVectors()

	def initiateRetreat(self): #still uses basicRetreat if no ally is
		Game=self.GameClass	   #available to retreat to.
		Tim=self.WarriorClass

		closestAllyNotOverPowered=self.getAlly()
		if closestAllyNotOverPowered==None:
			self.RetreatAwayFromEnemyCOF()
		else:
			self.moveTowardsAlly(closestAllyNotOverPowered)


class Explore(Strategy): #used if no enemy in sight to attack to.
						 #or all outposts under control. or both.

	def behave(self):
		self.setExplorationDestination()

	def setExplorationDestination(self): 
		Tim=self.WarriorClass
		step=100
		halfStep=50 #if above doesn't work, try this.
		angles=[0, math.pi/4, math.pi/2, math.pi*3/4, math.pi,
				math.pi*5/4, math.pi*3/2, math.pi*7/4]
		anglesToPick=copy.copy(angles)
		while True:
			if step==halfStep and angles==[]:
				Tim.destinations=[]
				return #exhausted all possibilities. don't crash. don't move.
			elif anglesToPick==[]:
				step //=2  					#we will try again. if doesn't work, the 
				anglesToPick=copy.copy(angles) #conditional before will come into play. 
			angle=random.choice(anglesToPick) #more vivid movement that list indexing.
			anglesToPick.remove(angle) 
			(dx, dy)=balanceVelocityIntoVectors(step, angle) #increments.
			if self.isValidExplorationDestination((Tim.x+dx, Tim.y+dy)):
				Tim.destinations=[(Tim.x+dx, Tim.y+dy)]
				Tim.getVelocityVectors()
				return 

	def isValidExplorationDestination(self, dest):
		Tim=self.WarriorClass
		Game=self.GameClass
		testPoints=isPathClearTestPoints((Tim.x, Tim.y), dest)
		for testPoint in testPoints:
			(x, y)=testPoint
			if doesPointIntersectWithSoldiers(testPoint, Game, Tim):
				return False
			elif doesPointIntersectWithObstacles(testPoint, Game, Tim.radius):
				return False
			elif self.isOutOfBounds(x, y):
				return False
		return True 

########################################################################
########################################################################
################### Attacking Strategies .. ############################
########################################################################
########################################################################

class FindClosestEnemy_Attack(Strategy): #most basic algorithm. it just works.

	def behave(self):
		self.handleAttack() #movement towards closest enemy.
		self.checkForEnemyWithinRange() #commence firing when in range.

	def handleAttack(self):
		Warrior=self.WarriorClass
		(closestEnemy, distance)=(self.findEnemyToAttack())
		if not closestEnemy==None:
			Warrior.destinations=[(closestEnemy.x, closestEnemy.y)] #overrides 
													#any existing destination
		Warrior.getVelocityVectors() 

	def findEnemyToAttack(self): #returns x,y of the closest enemy in range.
		#implement fog of war here.
		closestDistance=None
		enemyToAttack=None
		myCoordinates=(self.WarriorClass.x, self.WarriorClass.y)
		for Warrior in self.GameClass.Warriors:
			if Warrior.type!=self.WarriorClass.type:
				enemyCoordinates=(Warrior.x, Warrior.y)
				thisDistance=getDistance(myCoordinates, enemyCoordinates)
				if closestDistance==None or thisDistance<closestDistance:
					closestDistance=thisDistance 
					enemyToAttack=Warrior
		return (enemyToAttack, closestDistance)

	def checkForEnemyWithinRange(self): #does the actual firing.
		Tim=self.WarriorClass
		shootingRange=self.shootingRange
		(closestEnemy, distance)=(self.findEnemyToAttack())
		if closestEnemy==None: 
			(Tim.vx, Tim.vy)=(0,0) #Victorious. Relax.
			return 
		if distance<shootingRange:
			(Tim.vx, Tim.vy)=(0, 0) #stop and shoot.
			if self.checkIfClearShot(closestEnemy):
				if Tim.fireDelay==0:
					self.fire() 
					Tim.fireDelay=50 #back to start.


########################################################################
########################################################################
######################## Smarter (AI) Class ############################
########################################################################
########################################################################

#it works better, but still falls back on the first one when positioning
#is complete.

class shareEnemies(Strategy):

	def behave(self):
		self.runEnemyAllocator()

	def getAllies(self):
		allies=[]
		for Warrior in self.GameClass.Warriors:
			if Warrior.type==self.WarriorClass.type: #allies
				allies.append(Warrior)
		return allies 

	def getEnemies(self):
		enemies=[]
		for Warrior in self.GameClass.Warriors: #enemies
			if Warrior.type!=self.WarriorClass.type:
				enemies.append(Warrior)
		return enemies

	@staticmethod
	def getClosestAllyToEnemy(allies, enemy):
		enemyLoc=(enemy.x, enemy.y)
		closestDistance=None
		closestAllyThusFar=None
		for ally in allies:
			allyLoc=(ally.x, ally.y)
			thisDistance=getDistance(allyLoc, enemyLoc)
			if closestDistance==None or thisDistance<closestDistance:
				closestDistance=thisDistance
				closestAllyThusFar=ally
		return closestAllyThusFar

	def runEnemyAllocator(self):
		allies=self.getAllies()
		enemies=self.getEnemies()
		if len(enemies)==0: 
			self.WarriorClass.destinations=[] #Victorious.
			return
		while len(allies)>0: #continue until all allies are allocated to an enemy.
			for enemy in enemies:
				closestAlly=shareEnemies.getClosestAllyToEnemy(allies, enemy)
				if closestAlly==self.WarriorClass: #this is this class.
					self.WarriorClass.destinations=[(enemy.x, enemy.y)]
					self.WarriorClass.getVelocityVectors()
				allies.remove(closestAlly) #and re-do the allocation
				if len(allies)==0: 
					return #out of allies, end of allocation.

########################################################################
########################################################################

class surroundEnemies(shareEnemies): #uses Maze-Solver to surround Enemy.

	def runEnemyAllocator(self):   #same with shareEnemies except for get dest.
		allies=self.getAllies()	
		enemies=self.getEnemies()
		if len(enemies)==0: 
			self.WarriorClass.destinations=[] #Victorious.
			return
		while len(allies)>0: #continue until all allies are allocated to an enemy.
			for enemy in enemies:
				closestAlly=shareEnemies.getClosestAllyToEnemy(allies, enemy)
				if closestAlly==self.WarriorClass: #this is this class.
					self.WarriorClass.destinations=self.getDest(enemy)
					self.WarriorClass.getVelocityVectors()
				allies.remove(closestAlly) #and re-do the allocation
				if len(allies)==0: 
					return #out of allies, end of allocation.

	@staticmethod
	def getDestFromAngle(angle, enemy):
		shootingDistance=60
		(deltaX, deltaY)=balanceVelocityIntoVectors(shootingDistance, angle)
		return (enemy.x+deltaX, enemy.y+deltaY)


	def isValidDest(self, x, y):
		point1=(x, y)
		#does dest intersect with other soldier
		for Warrior in self.GameClass.Warriors:
			point2=(Warrior.x, Warrior.y)
			distance=getDistance((point1), (point2))
			if (Warrior.radius*2)>=distance:
				return False
		#does dest intersect with ally dest (they would have priority.)
		for Warrior in self.GameClass.Warriors:
			if not Warrior.type==self.WarriorClass.type: continue
			if Warrior.destinations==[]: continue #not set yet.
			point2=Warrior.destinations[0]
			distance=getDistance((point1), (point2))
			if (Warrior.radius*2)>=distance:
				return False 
		#if passed these tests:
		return True

	def getDest(self, enemy): #among the available surronding coordinates
							  #picks the closest one.
		myLoc=(self.WarriorClass.x, self.WarriorClass.y)
		angleIncrement=math.pi/4
		closestDistance=None
		closestCoordinates=None
		angle=0
		while angle<=math.pi*2:
			(x, y)=surroundEnemies.getDestFromAngle(angle, enemy)
			if self.isValidDest(x, y):
				distance=getDistance(myLoc, (x, y))
				if closestDistance==None or distance<closestDistance:
					closestDistance=distance
					closestCoordinates=(x,y)
			angle+=angleIncrement
		return [closestCoordinates] if closestCoordinates!=None else []

	