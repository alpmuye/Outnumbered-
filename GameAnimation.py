from Animation import Animation
from MapItems import Map 
from helperFunctions import *
from Squad import *
from mainAnimationHelpers import *

#a subclass of Animation that is fit for developing 
#actual levels.

class GameAnimation(Animation):

	def getModeChange(self, event): pass

	def initLevel(self, canvas): pass 

	def init(self, canvas):
		(self.width, self.height)=(1200,600)
		self.fogOfWarActive=True
		self.Warriors= []
		self.Map=Map()
		self.formationCoordinates=[]
		self.Squads=[]
		self.Outposts=[]
		drawMap(self, canvas)
		self.bullets=[]
		self.explosions=[]
		self.mouseMovements=[] #track to form selection rectangle.
		self.bulletMaxLifeTime=50
		self.isPaused=False

	def mouseMoved(self, event):
		if self.isPaused: return  
		loc=(event.x, event.y)
		self.mouseMovements.append(loc)
		if len(self.mouseMovements)>=2: #you need a rectangle first
			handleRectangleSelects(self)

	def mouseReleased(self, event):
		if self.isPaused: return 
		self.mouseMovements=[] #reset selection rectangle
		if self.formationCoordinates!=[]:
			if len(getSelectedWarriors(self))!=0: #don't crash by "/0"
				handleSelectedWarriorFormation(self)
				self.formationCoordinates=[] #reset

	def shiftMousePressed(self, event):
		if self.isPaused: return 
		(x,y)=(event.x, event.y)
		appendWarriorDestination(self, x, y)

	def shiftMouseMoved(self, event):
		if self.isPaused: return 
		(x,y)=(event.x, event.y)
		self.formationCoordinates.append((x,y))

	def mousePressed(self, event):
		if self.isPaused: return 
		(x,y)=(event.x, event.y)
		if handleWarriorSelects(self, x, y): return 
		if handleWarriorDestinations(self, x, y): return
		if handleSquadSelects(self, x, y): return 
		handleSquadDestinations(self, x, y)

	def redrawAll(self, canvas):
		drawOutposts(self, canvas)
		drawWarriors(self, canvas)
		drawBullets(self, canvas)
		if self.mouseMovements!=[]: drawSelectionRectangle(self, canvas)
		drawExplosions(self, canvas)
		drawLineFromFormationCoordinates(self, canvas)
		#pauseScreen.
		if self.isPaused:
			canvas.create_text(self.width/2, self.height/2, 
				text="Paused. Press P to unpause.", tags="delete")

	def timerFired(self):
		if self.isPaused: return  
		updateWarriors(self)
		updateBullets(self)
		updateExplosions(self)
		updateSquads(self)
		updateOutposts(self)

	def keyPressed(self, event): 
		if event.keysym=="p":
			self.isPaused=not self.isPaused 
		if event.keysym=="r":
			clearSelections(self)
		elif event.keysym=="s":
			handleSquadBindings(self)
		elif event.keysym=="Left" or event.keysym=="Right":
			handleSquadRotations(self, event)
