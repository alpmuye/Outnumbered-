
#Where everything comes together. Run this and you get a game.

from DotWarrior import *
from Animation import *
from DotWarrior import *
from Bullet import * 
from helperFunctions import *
from Squad import *
from DotWarrior import *
from MapItems import *
from mainAnimationHelpers import *
from GameAnimation import *
from Tutorials import *
from CampaignLevels import *
from Menus import *

##############################################################################
############################## The Game Class ################################
##############################################################################

class EndersGame(Animation):

	def init(self):
		self.mode="splashScreen"
		self.modes={"Tutorial": Tutorial(), 
					"splashScreen": splashScreen(),
					"Campaign": Campaign(),
					"TroopMovement": TroopMovement(),
					"SquadMovement":SquadMovement(), "Attacking":Attacking(),
					"Outposts":Outposts(), "FirstBattle":FirstBattle(),
					"OpenWarfare_I": OpenWarfare_I(),
					"OpenWarfare_II": OpenWarfare_II(),
					"Domination_I": Domination_I(),
					"Domination_II": Domination_II(),
					"Hell": Hell()}

		self.modes[self.mode].init(self.canvas) #for splash screen

	def mouseMoved(self, event):
		self.modes[self.mode].mouseMoved(event)

	def mouseReleased(self, event):
		self.modes[self.mode].mouseReleased(event)

	def shiftMousePressed(self, event):
		self.modes[self.mode].shiftMousePressed(event)

	def shiftMouseMoved(self, event):
		self.modes[self.mode].shiftMouseMoved(event)

	def mousePressed(self, event):
		newMode=self.modes[self.mode].getModeChange(event)
		if not newMode==None:
			self.canvas.delete(ALL) 
			self.mode=newMode
			self.modes[self.mode].init(self.canvas)
			return #don't do anything else in this timer fired.
		self.modes[self.mode].mousePressed(event)

	def redrawAll(self):
		canvas=self.canvas
		self.modes[self.mode].redrawAll(canvas)

	def timerFired(self):
		self.modes[self.mode].timerFired()

	def keyPressed(self, event): #these button presses work across all
		if event.keysym=="Escape": #animation classes.
			self.canvas.delete(ALL) 
			self.mode="splashScreen"
			self.modes[self.mode].init(self.canvas)
		elif event.keysym=="b":
			self.canvas.delete(ALL) 
			self.mode="Tutorial"
			self.modes[self.mode].init(self.canvas)
		elif event.keysym=="z":
			self.canvas.delete(ALL)
			self.modes[self.mode].init(self.canvas)
		elif event.keysym=="n":
			self.canvas.delete(ALL) 
			self.mode="Campaign"
			self.modes[self.mode].init(self.canvas)
		self.modes[self.mode].keyPressed(event)


##############################################################################
##############################  Splash Screen ################################
##############################################################################

def initSplashScreenButtons(self): 
	buttonBounds={}
	buttonSize=100
	buttonHeight=40
	buttonMargin=buttonHeight*2
	(cx, cy)=(self.width/2, self.height/2-buttonMargin)
	tutorialButton=( ((cx -buttonSize), (cy -buttonHeight)),
		((cx+buttonSize), (cy +buttonHeight)))
	buttonBounds["Tutorial"]=tutorialButton
	(cx, cy)=(self.width/2, self.height/2 +buttonMargin)
	campaignButton=( ((cx-buttonSize), (cy-buttonHeight)),
		((cx+buttonSize), (cy +buttonHeight)))
	buttonBounds["Campaign"]=campaignButton
	return buttonBounds

class splashScreen(GameAnimation):

	def levelInit(self, canvas):
		self.Warriors=[Red(100,100), Red(200,200), Red(300,300),
					   Red(150,150), Red(250,250), Red(350,350),
					   Red(100,180), Red(400,200), Red(400,300),
					   Red(500,180), Red(420,550), Red(470,380),
					   Red(500,250), Red(500,400), Red(500,350),]
		self.Map=Map()
		drawMap(self, canvas)

	def init(self, canvas):
		super().init(canvas)
		self.levelInit(canvas)
		self.buttons=initSplashScreenButtons(self)
		self.fogOfWarActive=False

	def mouseMoved(self, event): pass

	def mouseReleased(self, event): pass

	def shiftMousePressed(self, event): pass 

	def shiftMouseMoved(self, event): pass 

	def isClickInButtonBounds(self, x, y):
		for button in self.buttons:
			buttonBounds=self.buttons[button]
			bounds=(buttonBounds[0][0], buttonBounds[0][1], #unpacking values.
				buttonBounds[1][0], buttonBounds[1][1]) #I know. Ugh.
			if isDotInBounds(bounds, (x,y)):
				return button 
		#no button was pressed.
		return None

	def getModeChange(self, event): #Called by the main Class.
									#Checks for mode changes with each
									#mouse click, if there are any.

		button=self.isClickInButtonBounds(event.x, event.y)
		return button

	def mousePressed(self, event): pass 

	def redrawAll(self, canvas):
		super().redrawAll(canvas)
		canvas.create_text(self.width/2, self.height/7, 
			text="Outnumbered", tags="delete",
			     font="Times 36 bold")
		canvas.create_text(self.width/2, self.height/5, 
			text="by Alp Müye.", tags="delete",
			     font="Times 18", anchor=W)
		for button in self.buttons:
			canvas.create_rectangle(self.buttons[button], tags="delete",
								width=2)
			points=[] #get text center from button bounds.
			for point in self.buttons[button]:
				points.append(point)
			textCenter=getCenterPoint(*points)
			canvas.create_text(textCenter, text=button, tags="delete")

	def keyPressed(self, event): pass 

################################################################################
################################################################################

EndersGame().run(1200,600)