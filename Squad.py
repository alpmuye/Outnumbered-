from DotWarrior import *
from DotWarrior import *
from helperFunctions import *
import math
import random

#The squad class used to ease group movement for the player class.

class Squad(object):
	def __init__(self, Warriors):
		self.Warriors=Warriors
		self.color=random.choice(["black", "green", "purple", "magenta", 
							"maroon", "orange", "yellow"])
		self.getCenterOfMass()
		self.WarriorLocDict={} #stores the position of each warrior
							   #with respect to the Center of Mass.
		self.storeWarriorLocWithRespectToCOF()
		self.isSelected=False
		self.angularSpeed=math.pi/8

	def contains(self, x, y): #for mouseClicks
		for Warrior in self.Warriors: #click any and you're good.
			if Warrior.contains(x, y):
				return True
		return False

	def select_unselect(self):
		if self.isSelected:
			for Warrior in self.Warriors:
				Warrior.isSelected=True
		else: #not selected.
			for Warrior in self.Warriors:
				Warrior.isSelected=False

	def getCenterOfMass(self):
		massOfEachWarrior=1
		numOfWarriors=len(self.Warriors)
		if numOfWarriors==0: return #dead squad.
		xVectors=0
		yVectors=0
		for Warrior in self.Warriors:
			xVectors+=Warrior.x 
			yVectors+=Warrior.y 
		centerX=xVectors/numOfWarriors #times the mass of each, =1, so no point.
		centerY=yVectors/numOfWarriors
		self.CenterOfMass= (centerX, centerY)

	def storeWarriorLocWithRespectToCOF(self):
		COF=self.CenterOfMass
		(xCOF, yCOF)=COF
		for Warrior in self.Warriors:
			(deltaX, deltaY)= (xCOF-Warrior.x, yCOF-Warrior.y)
			angle=getAngleFromDeltas(deltaX, deltaY)
			distanceToCOF=getDistance((Warrior.x, Warrior.y), COF)
			self.WarriorLocDict[Warrior]=(distanceToCOF, angle)

	def changeCenterOfMass(self, x, y):
		#change the center of mass and also change the angle of each warrior
		#with respect to the old center of mass. (Rotate the squad!)
		(oldX, oldY)=self.CenterOfMass
		self.CenterOfMass=(x, y) #changed the center of mass.

	def rotateLeft(self):
		angle=self.angularSpeed
		(xCOF, yCOF)=self.CenterOfMass
		for Warrior in self.WarriorLocDict:
			(distance, oldAngle)=self.WarriorLocDict[Warrior]
			self.WarriorLocDict[Warrior]=(distance, oldAngle-angle)
			(distance, newAngle)=self.WarriorLocDict[Warrior]
			(dx,dy)=balanceVelocityIntoVectors(distance, newAngle)
			Warrior.setDestination(xCOF-dx, yCOF-dy)

	def rotateRight(self):
		angle=self.angularSpeed
		(xCOF, yCOF)=self.CenterOfMass
		for Warrior in self.WarriorLocDict:
			(distance, oldAngle)=self.WarriorLocDict[Warrior]
			self.WarriorLocDict[Warrior]=(distance, oldAngle+angle)
			(distance, newAngle)=self.WarriorLocDict[Warrior]
			(dx,dy)=balanceVelocityIntoVectors(distance, newAngle)
			Warrior.setDestination(xCOF-dx, yCOF-dy)

	def update(self):
		self.select_unselect()
		self.getCenterOfMass()
		self.storeWarriorLocWithRespectToCOF()

