
from GameAnimation import *
import random


################################################################################
####################    The Levels in the Campaign  ############################
################################################################################


################################################################################
#							Some Helper Functions
################################################################################

def anyRedWarriorsLeft(self):
	for Warrior in self.Warriors:
		if Warrior.type=="enemy":
			return True
	self.winner="player" 
	return False

def anyBlueWarriorsLeft(self):
	for Warrior in self.Warriors:
		if Warrior.type=="player": 
			return True
	self.winner="enemy"
	return False

################################################################################
#							Elimination Game Class
################################################################################

class EliminationGame(GameAnimation): #type of game which you win by 
									  #destroying all enemy soldiers.
									  #dead soldiers do not revive.
	def isGameOver(self):
		if not anyRedWarriorsLeft(self):
			return True
		elif not anyBlueWarriorsLeft(self):
			return True 
		return False

	def redrawAll(self, canvas):
		super().redrawAll(canvas)
		if self.GameOver:
			text= "VICTORIOUS" if self.winner=="player" else "YOU JUST GOT OWNED."
			canvas.create_text(self.width/2, self.height/2,
				text=text, tags="delete", font="Times 36 bold")
			canvas.create_text(self.width/2, self.height/1.5, tags="delete",
				font="Times 20", text=" Press Z to play again, B for tutorial menu")
			canvas.create_text(self.width/2, self.height/1.3, tags="delete",
				font="Times 20", text="N for campaign menu, and Escape for main menu.")

################################################################################
#						The Domination Game Class
################################################################################

class DominationGame(GameAnimation): #type of game where there is a timer 
									 #a score, and soldiers revive.
									 #most points at the end of the timer
									 #wins the game.

	#You can also win by K.O, completely destroying the enemy before it 
	#has a chance to revive. But that is kind of unlikely. But possible.

	def init(self, canvas):
		super().init(canvas)
		self.timer=6000 #50 step = 1 second. Ideally. It tends to slow down.
		self.blueRevivalQueue=[]
		self.redRevivalQueue=[]
		self.GameOver=False
		self.isByKO=False
		self.blueScore=0
		self.redScore=0

	def isGameOverByKO(self):
		if not anyRedWarriorsLeft(self):
			return True
		elif not anyBlueWarriorsLeft(self):
			return True 
		return False

	def getWinner(self):
		return "You win!" if self.blueScore>self.redScore else "You lost."

	def isTimeFinished(self):
		if self.timer<=0:
			self.timer=0
			self.GameOver=True 

#a list of digits that gets decreased, each turn, 
#and removed when it hits zero, also 
#produces a warrior of that class. 
	def reviveTimers(self):
		for i in range(len(self.blueRevivalQueue)):
			self.blueRevivalQueue[i]-=1
		for i in range(len(self.redRevivalQueue)):
			self.redRevivalQueue[i]-=1

	def getKillPoints(self):
		reviveTime=200
		for Warrior in self.Warriors:
			if Warrior.healthPoints<=0:
				if Warrior.type=="enemy":
					self.blueScore+=5
					self.redRevivalQueue.append(reviveTime)
				elif Warrior.type=="player":
					self.redScore+=5
					self.blueRevivalQueue.append(reviveTime)

	def getOutpostPoints(self): #points from captured outposts.
		for Outpost in self.Outposts:
			if Outpost.Occupier=="blue":
				self.blueScore+=0.05
			elif Outpost.Occupier=="red":
				self.redScore+=0.05

	def timerFired(self):
		if self.isPaused: return 
		if self.GameOver: return
		self.getOutpostPoints()
		self.getKillPoints() 
		super().timerFired()
		self.timer-=2
		if self.isGameOverByKO(): 
			self.GameOver=True
			self.isByKO=True #this is not related to points.
			return 				#KO is knock out. Total annhilation of 
								#enemy forces.
		self.isTimeFinished()
		self.reviveTimers()
		self.checkForRevives()

	def checkForRevives(self):
		self.reviveRed()
		self.reviveBlue()

	def reviveRed(self, canvas):
		pass
		#modify these in the level function according to the AI used.
	def reviveBlue(self, canvas):
		pass

	def drawTimer(self, canvas):
		panelAxis=580
		text= "Time Remaining: %d" % (self.timer//100) #convert it into seconds.
		canvas.create_text(self.width/2 ,panelAxis, text=text,font="Times 20 bold",
					tags="delete") #Fonts increased through Tuesday's peer review.

	def drawGameOver(self, canvas):
		if self.GameOver:
			if self.isByKO:
				text= "VICTORIOUS" if self.winner=="player" else "YOU JUST GOT OWNED."
				canvas.create_text(self.width/2, self.height/2,
					text=text, tags="delete", font="Times 36 bold")
			else: #won by time-over/ domination.
				canvas.create_text(self.width/2, self.height/2,
					text=self.getWinner(), tags="delete", font="Times 36 bold")
			canvas.create_text(self.width/2, self.height/1.5, tags="delete",
				font="Times 20", text=" Press Z to play again, B for tutorial menu")
			canvas.create_text(self.width/2, self.height/1.3, tags="delete",
				font="Times 20", text="N for campaign menu, and Escape for main menu.")

	def drawPoints(self, canvas):
		panelAxis=580
		(BlueX, RedX)=(450,750)
		text="Blue: %d" %(self.blueScore//1) #no floats.
		canvas.create_text(BlueX, panelAxis, text=text,
			font="Times 20", tags="delete")
		text="Red: %d" %(self.redScore//1) 
		canvas.create_text(RedX, panelAxis, text=text,
			font="Times 20", tags="delete")
		#Fonts increased through Tuesday's peer review.

	def redrawAll(self, canvas):
		super().redrawAll(canvas)
		self.drawTimer(canvas)
		self.drawGameOver(canvas)
		self.drawPoints(canvas)

###################################################################
#						Level 1 (Elimination)
###################################################################

class OpenWarfare_I(EliminationGame):

	def getBlueSoldiers(self, soldiers):
		blueSoldiers=[]
		step=0
		midX=self.width/2
		margin=30
		cy=500
		while soldiers>step:
			step+=1
			blueSoldiers.append(Blue(midX+margin*step, cy))
			blueSoldiers.append(Blue(midX-margin*step, cy))
		return blueSoldiers

	def getRedSoldiers(self, soldiers): #produces: smartRed
		redSoldiers=[]
		step=0
		midX=self.width/2
		margin=30
		cy=100
		while soldiers>step:
			step+=1
			redSoldiers.append(SmarterRed(midX+margin*step, cy))
			redSoldiers.append(SmarterRed(midX-margin*step, cy))
		return redSoldiers

	def levelInit(self, canvas):
		self.Warriors= self.getBlueSoldiers(3) + self.getRedSoldiers(5)
		self.Map=Map()
		self.Map.items=self.Map.getRandomTrees((0,1200,200,400), 10)
		drawMap(self, canvas)

	def timerFired(self):
		super().timerFired()
		if self.isGameOver(): self.GameOver=True

	def init(self, canvas):
		super().init(canvas)
		self.levelInit(canvas)
		self.GameOver=False
		self.fogOfWarActive=False


####################################################################
#						Level 2 (Elimination)
####################################################################

class OpenWarfare_II(OpenWarfare_I):
	def levelInit(self, canvas):
		self.Warriors= self.getBlueSoldiers(4) + self.getRedSoldiers(5)
		self.Map=Map()
		self.Map.items=self.Map.getRandomTrees((0,1200,200,400), 3)
		drawMap(self, canvas)

	def getRedSoldiers(self, soldiers): #produces: smartestRed
		redSoldiers=[]
		step=0
		midX=self.width/2
		margin=30
		cy=100
		while soldiers>step:
			step+=1
			redSoldiers.append(SmartestRed(midX+margin*step, cy))
			redSoldiers.append(SmartestRed(midX-margin*step, cy))
		return redSoldiers


####################################################################
#						Level 3 (Domination)
####################################################################

class Domination_I(DominationGame):

	def getBlueSoldiers(self, soldiers):
		blueSoldiers=[]
		step=0
		midY=self.height/2
		margin=30
		cx=100
		while soldiers>step:
			step+=1
			blueSoldiers.append(Blue(cx, midY+margin*step))
			blueSoldiers.append(Blue(cx, midY-margin*step))
		return blueSoldiers

	def getRedSoldiers(self, soldiers):
		redSoldiers=[]
		step=0
		midY=self.height/2
		margin=30
		cx=1000
		while soldiers>step:
			step+=1
			redSoldiers.append(SmarterRed(cx, midY+margin*step))
			redSoldiers.append(SmarterRed(cx, midY-margin*step))
		return redSoldiers

	def WarriorInit(self):
		return (self.getRedSoldiers(2) + self.getBlueSoldiers(4)
						+ [InvaderRed(900,300), InvaderRed(900,350)])

	def initLevel(self, canvas):
		self.Warriors=self.WarriorInit()
		self.Outposts=[Outpost(120,120), Outpost(1080,120),
							Outpost(600,200)]
		self.Map=Map()
		self.Map.items= [Hill(200,200), Hill(1000,200),
						Hill(600,300)]
		drawMap(self, canvas)

	def init(self, canvas):
		super().init(canvas)
		self.initLevel(canvas)

	def reviveRed(self):

		if self.redRevivalQueue==[]: return 
		if self.redRevivalQueue[0]<=0: #first in line.
			self.redRevivalQueue.pop(0) #first one out.
			minRespawnDif=100
			#new 0th index is the next one on the respawn list.
			if not self.redRevivalQueue==[]: #if not emptied list.
				if self.redRevivalQueue[0]<minRespawnDif: #for simulteneous deaths
					self.redRevivalQueue[0]=minRespawnDif #spawns should not overlap.
			if tossCoin():					    
				self.Warriors.append(SmarterRed(1180,580)) #revive loc
			else:										#right bottom corner.
				self.Warriors.append(InvaderRed(1180,580))
			destX=1000
			destY=random.randint(200,400)
			self.Warriors[-1].destinations=[(destX,destY)]
			self.Warriors[-1].getVelocityVectors() #so that revived 
											#soldiers don't overlap

	def reviveBlue(self):
		if self.blueRevivalQueue==[]: return 
		if self.blueRevivalQueue[0]<=0: #first in line.
			minRespawnDif=100
			self.blueRevivalQueue.pop(0) #first one out.
			if not self.blueRevivalQueue==[]:
				if self.blueRevivalQueue[0]<minRespawnDif: 
					self.blueRevivalQueue[0]=minRespawnDif 
			self.Warriors.append(Blue(20,580)) #revive loc
			destX=250					  #left bottom corner.
			destY=random.randint(200,400)
			self.Warriors[-1].destinations=[(destX,destY)]
			self.Warriors[-1].getVelocityVectors()

####################################################################
#						Level 4 (Domination)
####################################################################

class Domination_II(Domination_I): #Different map, smarter AI.

	def getBlueSoldiers(self, soldiers):
		blueSoldiers=[]
		step=0
		midY=self.height/2
		margin=30
		cx=100
		while soldiers>step:
			step+=1
			blueSoldiers.append(Blue(cx, midY+margin*step))
			blueSoldiers.append(Blue(cx, midY-margin*step))
		return blueSoldiers

	def getRedSoldiers(self, soldiers):
		redSoldiers=[]
		step=0
		midY=self.height/2
		margin=30
		cx=1000
		while soldiers>step:
			step+=1
			redSoldiers.append(SmartestRed(cx, midY+margin*step))
			redSoldiers.append(SmartestRed(cx, midY-margin*step))
		return redSoldiers

	def WarriorInit(self):
		return (self.getRedSoldiers(5) + self.getBlueSoldiers(4)
						+ [InvaderRed(900,300), InvaderRed(900,350)])

	def initLevel(self, canvas):
		self.Warriors=self.WarriorInit()
		self.Outposts=[Outpost(self.width/2, self.height/2)]
		self.Map=Map()
		self.Map.items= [Mountain(400,300), Mountain(600,500), 
							Mountain(600,100)]
		drawMap(self, canvas)

	def init(self, canvas):
		super().init(canvas)
		self.initLevel(canvas)

	def reviveRed(self):

		if self.redRevivalQueue==[]: return 
		if self.redRevivalQueue[0]<=0: #first in line.
			self.redRevivalQueue.pop(0) #first one out.
			minRespawnDif=100
			#new 0th index is the next one on the respawn list.
			if not self.redRevivalQueue==[]: #if not emptied list.
				if self.redRevivalQueue[0]<minRespawnDif: #for simulteneous deaths
					self.redRevivalQueue[0]=minRespawnDif #spawns should not overlap.
			if tossCoin():					    
				self.Warriors.append(SmartestRed(1170,500)) #revive loc
			else:
				self.Warriors.append(InvaderRed(1170,500))
			destX=1000
			destY=random.randint(200,400)
			self.Warriors[-1].destinations=[(destX,destY)]
			self.Warriors[-1].getVelocityVectors() #so that revived 
											#soldiers don't overlap
	
####################################################################
#						Level 5 (Elimination)
####################################################################

class Hell(OpenWarfare_II):
	def levelInit(self, canvas):
		self.Warriors= self.getBlueSoldiers(4) + self.getRedSoldiers(10)
		self.Map=Map()
		drawMap(self, canvas)

	