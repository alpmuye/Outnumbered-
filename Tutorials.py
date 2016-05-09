
from GameAnimation import *
from CampaignLevels import anyRedWarriorsLeft
from CampaignLevels import anyBlueWarriorsLeft

#The tutorial levels.

##############################################################################

#copy pasted from Campaign levels to prevent mutual importing.

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
##############################################################################


def drawInstructions(instruction, cx, cy, canvas):
	canvas.create_text(cx, cy, text=instruction, font="Times 16" ) 


##############################################################################

class TroopMovement(GameAnimation):

	def instructionsInit(self, canvas):
		ins="""
		-Click on troop to select

		-Click anywhere on map to command movement.

		-Shift click to queue movement orders, and keep single troop selected 
		 after order.

		-Press B to go back to complete the other tutorials!!

		"""
		drawInstructions(ins, self.width/7, 300, canvas)


	def levelInit(self, canvas):
		self.Warriors=[Blue(self.width/2, self.height/2)]
		self.Map=Map()
		self.instructionsInit(canvas)

	def init(self, canvas):
		super().init(canvas)
		self.levelInit(canvas)

##############################################################################

def drawTrialFormation(canvas):
	ins="""
	-----------------------------------------------
	"""
	drawInstructions(ins, 600, 100, canvas)

class SquadMovement(GameAnimation):

	def instructionsInit(self, canvas):
		ins="""
		-Hold mouse to draw rectangle and select multiple troops.
		-Press R to de-select. 

		-Command troops to move to the sign below.

		-If you want them to line up in a particular way,
		hold shift, and draw a line, your troops will fill it up!
		Try lining them up filling the line above!!!

		- Press S to bind/unbind the selected troops into a squad.

		- Squads will retain formation when ordered to move!

		- You can rotate squads with the left & righ arrow keys.

		- You can change squad formations with shift clicks anytime!

		- You cannot order squads to attack single enemies, squads are 
		  for positioning only!

		-Press B to go back to complete the other tutorials!!

		"""
		drawInstructions(ins, self.width/7, 300, canvas)
		canvas.create_text(self.width/2, 500, text="Move here!")
		drawTrialFormation(canvas)

	def levelInit(self, canvas):
		self.Warriors=[Blue(600,300), Blue(650,300), Blue(550,300),
								Blue(500,300), Blue(700,300)]
		self.Map=Map()
		self.instructionsInit(canvas)

	def init(self, canvas):
		super().init(canvas)
		self.levelInit(canvas)


########################################################################

class Attacking(GameAnimation):
	def instructionsInit(self, canvas):
		ins="""
		Select your troop and order it to attack these troops.
		(By clicking of course!)

		If your warrior is not selected, but within range of enemy,
		it will attack it automatically (You don't have to order!)

		But if it is selected, and you don't order it to attack,
		it will not attack! Make sure to de-select for auto-pilot!
		Pressing R at the right time to de-select can make all the difference!!!

		The more you flank, the more hit points you get!

		Your life points correlate to your hit points!
		"""
		drawInstructions(ins, 300, 350, canvas)

	def levelInit(self, canvas):
		self.Warriors=[Blue(100,100), Blue(150, 100), TutorialRed(300,305),
			TutorialRed(350,305), TutorialRed(380,305), TutorialRed(270,305)]
		self.Map=Map()
		self.instructionsInit(canvas)

	def timerFired(self):
		super().timerFired()
		

	def init(self, canvas):
		super().init(canvas)
		self.levelInit(canvas)
		self.hasDrawed=False

	def newInstructions(self, canvas):
		for Warrior in self.Warriors:
			if type(Warrior)==TutorialRed: return
		ins="""

		Now with a real enemy. Make sure your troops
		don't block each other's shooting. Make sure
		you are not flanked. Try out line formations,
		and squad managements. 

		Don't forget, troops regenerate over time!

		Press B to go back and finish the tutorial!  

		"""
		if not self.hasDrawed: #so that it draws it only once.
			canvas.delete(ALL)
			drawMap(self, canvas)
			drawInstructions(ins, self.width/2, self.height/2, canvas)	
			self.hasDrawed=True
			return
		for Warrior in self.Warriors:
			if type(Warrior)==Red: return
		self.Warriors.append(Red(1000,100))

	def redrawAll(self, canvas):
		super().redrawAll(canvas)
		self.newInstructions(canvas)

############################################################################

class Outposts(GameAnimation):

	# introduce each map item

	def instructionsInit(self, canvas):
		ins="""
		Here are different types of map items.

		You cannot see through trees and mountains.

		Trees and hills slow you down. 

		Attacking from hills to enemies that are not hills
		gives an attacking bonus.

		Try to capture both outposts on the map by occupying them. 







		Oh by the way, you won't see enemies unless they are in range,
		and not behind opaque map items. Good luck :)

		""" # I probably could have used \n but meh. 
		drawInstructions(ins, self.width/7, self.height/2, canvas)

	def levelInit(self, canvas):
		self.Warriors=[Blue(100,100), Blue(50,100), Blue(150,100), Blue(20,20),
			SmartestRed(1000,50), SmartestRed(1000,100), InvaderRed(1050,100)]
		self.Map=Map()
		self.Map.items=(self.Map.getRandomTrees((500,600,300,500), 5) + 
								  self.Map.getRandomRocks((500,600),5) + 
					[Mountain(500,200), Hill(1000,400), Hill(650,100)])
		drawMap(self, canvas)
		self.instructionsInit(canvas)
		self.Outposts=[Outpost(200,400), Outpost(800,450)]

	def init(self, canvas):
		super().init(canvas)
		self.levelInit(canvas)

##############################################################################

class FirstBattle(EliminationGame):

	def levelInit(self, canvas):
		self.Warriors= self.getBlueSoldiers() + self.getRedSoldiers()
		self.Map=Map()
		self.Map.items=[Mountain(600,300), Hill(300,150), Hill(300,450),
						Hill(900, 150), Hill(900,450)]
		drawMap(self, canvas)
	
	def getBlueSoldiers(self):
		return [Blue(100,50), Blue(100,100), Blue(100,150), Blue(100,200),
							Blue(100,250), Blue(100,300)]

		#these two functions for the first battle game in the tutorial.

	def getRedSoldiers(self):
		return [SmarterRed(1000,50), SmarterRed(1000,100), SmarterRed(1000,150), 
				    SmarterRed(1000,200), SmarterRed(1000,250), SmarterRed(1000,300),
				    SmarterRed(1000,350)]
	
	def timerFired(self):
		super().timerFired()
		if self.isGameOver(): self.GameOver=True

	def init(self, canvas):
		super().init(canvas)
		self.levelInit(canvas)
		self.GameOver=False

##############################################################################