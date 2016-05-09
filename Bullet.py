
import math 
import random
from helperFunctions import *
from MapItems import *

# Bullet and the explosion class.

####################################################################################
			#################### Explosion ############################
####################################################################################

class Explosion(object):
	def __init__(self, x, y):
		self.x=x
		self.y=y 
		self.radius=1

	def update(self): #grow with each update until destruction.
		self.radius+=1

	def draw(self, canvas):
		(cx, cy, r)=(self.x, self.y, self.radius)
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="yellow",
			tags="delete")
		#inner fire.
		r=r/2
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="red",
			tags="delete")

####################################################################################
	########################### Pew, Pew! ####################################
####################################################################################

class Bullet(object):
	def __init__(self, x, y, angle, firingWarrior):
		self.x=x
		self.y=y
		self.angle=angle
		self.firingWarrior=firingWarrior
		self.radius=2
		self.velocity=4
		(self.vx, self.vy)=balanceVelocityIntoVectors(self.velocity, self.angle)
		self.lifeTime=0

	def move(self):
		self.x+=self.vx
		self.y+=self.vy 

	def getHitPoints(self): #depends on your strength, and luck.
		hitPointRatio=3 #for division in calculating the range.
		healthPoints=self.firingWarrior.healthPoints
		averageHitPoint=healthPoints//10 
		hitRange=averageHitPoint//hitPointRatio
		minHitPoints= averageHitPoint-hitRange
		maxHitPoints= averageHitPoint+hitRange 
		try: return random.randint(minHitPoints, maxHitPoints)
		except: #if range is not valid:
			return averageHitPoint
		#enough luck to make it interesting, but still make it mostly strategy.

	def getHillChargeBonus(self, Warrior, data):
		hillBonus=8
		attacker=self.firingWarrior
		enemyLoc=(Warrior.x, Warrior.y)
		for item in data.Map.items: #no bonus if enemy also on hill.
			if item.contains(Warrior.x, Warrior.y):
				if type(item)==Hill: 
					return 0
		for item in data.Map.items: #no bonus if enemy also on hill.
			if item.contains(attacker.x, attacker.y):
				if type(item)==Hill:
					return hillBonus
		return 0 

	def getFlankingBonus(self, Warrior):
		angle=(Warrior.headAngle)
		(cx, cy)=(Warrior.x, Warrior.y)
		(deltaX, deltaY)=(cx-self.x, cy-self.y)
		angleHit=getAngleFromDeltas(deltaX, deltaY)
		#equalize all the angles until they are 0<=angle<=2*math.pi
		while angle<0: angle+=math.pi*2 
		while angle>math.pi*2: angle-=math.pi*2
		while angleHit<0: angleHit+=math.pi*2 
		while angleHit>math.pi*2: angleHit-=math.pi*2
		deltaAngle=abs(abs(angle-angleHit)-math.pi) 
		flankingFactor=5
		return deltaAngle*flankingFactor

	def hitSoldier(self, Warrior, data):
		hitPoint=self.getHitPoints()
		hitPoint+=self.getFlankingBonus(Warrior)
		hitPoint+=self.getHillChargeBonus(Warrior, data)
		Warrior.healthPoints-=hitPoint 

	def didHitSoldier(self, data):
		for Warrior in data.Warriors:
			point1=(self.x, self.y)
			point2=(Warrior.x, Warrior.y)
			distance=getDistance(point1, point2)
			if distance<=(self.radius+Warrior.radius):
				if Warrior!=self.firingWarrior: #don't hit yourself..
					self.hitSoldier(Warrior, data)
					return True
		return False

	def update(self, data):
		maxLifeTime=data.bulletMaxLifeTime
		if self.didHitSoldier(data): 
			self.lifeTime=maxLifeTime #bullet will be removed in the main class.
		else: 
			self.lifeTime+=1
		self.move()

	def draw(self, canvas):
		(cx, cy, r)=(self.x, self.y, self.radius)
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="black",
			tags="delete")
