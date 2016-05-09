from Animation import *
from helperFunctions import *

#Menu classes, buttons, and stuff.

def getButtonBounds(cx, cy, buttonHeight):
	buttonSize=90
	return (((cx-buttonSize), (cy-buttonHeight)),
		((cx+buttonSize), (cy +buttonHeight)))

def initTutorialButtons(self, canvas): 
	buttonBounds={}
	buttonHeight=90
	(cxFactor, cy)=(self.width/6, self.height/2)
	cy=self.height/2
	levelNameMargin=30
	for factor in range(5):
		cx=factor*cxFactor +cxFactor
		self.levelListLoc.append((cx, cy+buttonHeight+levelNameMargin))
		buttonBounds[str(factor)]=getButtonBounds(cx, cy, buttonHeight)
		self.buttonCenters.append((cx, cy))
	return buttonBounds

class Tutorial(Animation):

	def init(self, canvas):
		super().init()
		self.levelListLoc=[]
		self.buttonCenters=[]
		self.buttons=initTutorialButtons(self, canvas)
		self.drawButtonImages(canvas)
		self.drawLevelNames(canvas)
		self.levels=["TroopMovement", "SquadMovement", "Attacking",
					"Outposts", "FirstBattle"]

	def createModelTree(self, canvas, cx, cy):
		r=10
		thickness=3
		canvas.create_rectangle(cx-thickness, cy, cx+thickness,
								cy+20, fill="brown")
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="green")

	def drawButtonImages(self, canvas):
		(cx, cy)= self.buttonCenters[0]
		self.drawModelWarrior(canvas, cx, cy, 30, "blue")
		(cx, cy)= self.buttonCenters[1]
		self.drawModelWarrior(canvas, cx-25, cy, 20, "blue")
		self.drawModelWarrior(canvas, cx+25, cy, 20, "blue")
		self.drawModelWarrior(canvas, cx, cy-35, 20, "blue")
		self.drawModelWarrior(canvas, cx, cy+35, 20, "blue")
		(cx, cy)= self.buttonCenters[2]
		self.drawModelWarrior(canvas, cx, cy, 20, "red")
		(cx, cy)= self.buttonCenters[3]
		self.createModelTree(canvas, cx, cy)
		self.createModelTree(canvas, cx-20, cy)
		self.createModelTree(canvas, cx+20, cy)
		(cx, cy)= self.buttonCenters[4]
		self.drawModelWarrior(canvas, cx-25, cy, 20, "blue")
		self.drawModelWarrior(canvas, cx+25, cy, 20, "red")

	def isClickInButtonBounds(self, x, y):
		for button in self.buttons:
			buttonBounds=self.buttons[button]
			bounds=(buttonBounds[0][0], buttonBounds[0][1], #unpacking values.
				buttonBounds[1][0], buttonBounds[1][1]) #I know. Ugh.
			if isDotInBounds(bounds, (x,y)):
				return button

	def getModeChange(self, event):
		
		button=self.isClickInButtonBounds(event.x, event.y)
		if not button==None:
			return self.levels[int(button)]
		else: return None

	def drawLevelNames(self, canvas):
		canvas.create_text(self.levelListLoc[0], text="Troop Control&Movement")
		canvas.create_text(self.levelListLoc[1], text="Group Movement&Squads")
		canvas.create_text(self.levelListLoc[2], text="Attacking & Enemy AI")
		canvas.create_text(self.levelListLoc[3], text="Outposts & Map Items")
		canvas.create_text(self.levelListLoc[4], text="Your First Battle!")

	def redrawAll(self, canvas):
		canvas.create_text(self.width/6, self.height/8, 
			text="Press Escape to go back to the main menu",
						 font="Times 18", tags="delete")
		for button in self.buttons:
			canvas.create_rectangle(self.buttons[button], tags="delete",
								width=2)

################################################################################

class Campaign(Animation): #The campaign game menu.
	def init(self, canvas):
		super().init()
		self.levelListLoc=[]
		self.buttonCenters=[]
		self.buttons=initTutorialButtons(self, canvas)
		self.drawLevelNames(canvas)
		self.drawButtonImages(canvas)
		self.levels=["OpenWarfare_I", "OpenWarfare_II", "Domination_I",
					"Domination_II", "Hell"]

	def drawHell(self, canvas): #One does not simply soft-code the hell.
		(cx, cy)= self.buttonCenters[4]
		self.drawModelWarrior(canvas, cx-40, cy-20, 15, "red")
		self.drawModelWarrior(canvas, cx+40, cy-20, 15, "red")
		self.drawModelWarrior(canvas, cx, cy-20, 15, "red")
		self.drawModelWarrior(canvas, cx-75, cy-20, 15, "red")
		self.drawModelWarrior(canvas, cx+75, cy-20, 15, "red")
		self.drawModelWarrior(canvas, cx-40, cy+20, 15, "red")
		self.drawModelWarrior(canvas, cx+40, cy+20, 15, "red")
		self.drawModelWarrior(canvas, cx, cy+20, 15, "red")
		self.drawModelWarrior(canvas, cx-75, cy+20, 15, "red")
		self.drawModelWarrior(canvas, cx+75, cy+20, 15, "red")
		self.drawModelWarrior(canvas, cx-40, cy-60, 15, "red")
		self.drawModelWarrior(canvas, cx+40, cy-60, 15, "red")
		self.drawModelWarrior(canvas, cx, cy-60, 15, "red")
		self.drawModelWarrior(canvas, cx-40, cy+60, 15, "red")
		self.drawModelWarrior(canvas, cx+40, cy+60, 15, "red")
		self.drawModelWarrior(canvas, cx, cy+60, 15, "red")

	def drawOW2(self, canvas):
		(cx, cy)= self.buttonCenters[1]
		self.drawModelWarrior(canvas, cx-20, cy+20, 15, "blue")
		self.drawModelWarrior(canvas, cx+20, cy+20, 15, "blue")
		self.drawModelWarrior(canvas, cx-40, cy-20, 15, "red")
		self.drawModelWarrior(canvas, cx+40, cy-20, 15, "red")
		self.drawModelWarrior(canvas, cx, cy-20, 15, "red")

	def drawModelOutpost(self, canvas, cx, cy):
		r=70 #radius of the fake outpost
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r)
		r=20 #black outpost color
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="black")

	def drawButtonImages(self, canvas):
		(cx, cy)= self.buttonCenters[0]
		self.drawModelWarrior(canvas, cx-20, cy+20, 15, "blue")
		self.drawModelWarrior(canvas, cx+20, cy+20, 15, "blue")
		self.drawModelWarrior(canvas, cx-20, cy-20, 15, "red")
		self.drawModelWarrior(canvas, cx+20, cy-20, 15, "red")
		self.drawOW2(canvas)
		(cx, cy)= self.buttonCenters[2]
		self.drawModelOutpost(canvas, cx, cy)
		self.drawModelWarrior(canvas, cx-25, cy, 20, "blue")
		self.drawModelWarrior(canvas, cx+25, cy, 20, "red")
		(cx, cy)= self.buttonCenters[3]
		self.drawModelOutpost(canvas, cx, cy)
		self.drawModelWarrior(canvas, cx-25, cy, 15, "blue")
		self.drawModelWarrior(canvas, cx+25, cy, 15, "red")
		self.drawModelWarrior(canvas, cx, cy+40, 15, "red")
		self.drawModelWarrior(canvas, cx, cy-40, 15, "red")
		self.drawHell(canvas)
		
	def redrawAll(self, canvas):
		canvas.create_text(self.width/6, self.height/8, 
			text="Press Escape to go back to the main menu",
						 font="Times 18", tags="delete")
		for button in self.buttons:
			canvas.create_rectangle(self.buttons[button], tags="delete",
								width=2)

	def drawLevelNames(self, canvas):
		canvas.create_text(self.levelListLoc[0], text="Open Warfare")
		canvas.create_text(self.levelListLoc[1], text="Open Warfare 2.0")
		canvas.create_text(self.levelListLoc[2], text="Dominate the Map")
		canvas.create_text(self.levelListLoc[3], text="Dominate the Map 2.0")
		canvas.create_text(self.levelListLoc[4], text="Hell Beta")

	def getModeChange(self, event):
		button=self.isClickInButtonBounds(event.x, event.y)
		if not button==None:
			return self.levels[int(button)]
		else: return None

	def isClickInButtonBounds(self, x, y):
		for button in self.buttons:
			buttonBounds=self.buttons[button]
			bounds=(buttonBounds[0][0], buttonBounds[0][1], #unpacking values.
				buttonBounds[1][0], buttonBounds[1][1])
			if isDotInBounds(bounds, (x,y)):
				return button 