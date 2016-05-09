
import random
from DotWarrior import *
from helperFunctions import *

class Map(object):
#collects all the obstacles on a background, presents it to the game.
	def __init__(self):
		self.items=[]

	def checkIfPointIntersectAnyItem(self, x ,y): #make sure that there is no 
									   #item at the place where you are 
									   #randomly generating one.
		try:
			for item in self.items:
				if item.contains(x, y):
					return True 
			return False 
		except:
			return False
	
	def getRandomRocks(self, bounds, count):
		(boundX, boundY)=bounds
		rocks=[]
		for num in range(count):
			while True:
				x=random.randint(boundX, boundY)
				y=random.randint(boundX, boundY)
				if not self.checkIfPointIntersectAnyItem(x, y):
					rocks.append(Rock(x,y))
					break
		return rocks 

	def getRandomTrees(self, bounds, count):
		trees=[]
		(x1, x2, y1, y2)=bounds
		for num in range(count):
			while True:
				x=random.randint(x1, x2)
				y=random.randint(y1, y2)
				if not self.checkIfPointIntersectAnyItem(x, y):
					trees.append(Tree(x,y))
					break
		return trees

class Obstacle(object):
	def __init__(self, x ,y):
		self.x=x #Center Points
		self.y=y

	def draw(self): pass 

	def isPointWithinBoundaries(self, headPoint): pass

	def contains(self, x, y): #for Mouse clicks
		distance= getDistance((self.x, self.y), (x,y))
		return distance<=self.radius
 
class Mountain(Obstacle):

	def __init__(self, x, y):
		super().__init__(x,y)
		self.radius=random.randint(50,80)
		self.isTransparent=False
		self.isMovable=False

	def draw(self, canvas):
		(cx, cy, r)=(self.x, self.y, self.radius)
		#outer greens
		green=100
		R=r
		while R>(r*2/3):
			color=rgbString(0, green, 0)
			canvas.create_oval(cx-R, cy-R, cx+R, cy+R, fill=color, width=0)
			R-=4
			green+=5
		#inner brown
		red=140
		green=70
		R=r/2.5
		while R>0:
			if red<=60: red=60
			if green<=30: green=30 #No color code crashes.
			color=rgbString(red, green, 0)
			canvas.create_oval(cx-R, cy-R, cx+R, cy+R, fill=color, width=0)
			R-=1
			red-=3
			green-=3


class Tree(Obstacle): #not see through, but you can walk in it.
					  #slow movement

	def __init__(self, x, y):
		super().__init__(x,y)
		self.isTransparent=False
		self.isMovable=True 
		self.slowDownFactor=0.3  
		self.radius=random.randint(6,9)
		self.trunkSize=2
		self.trunkLength=random.randint(13,16)
		green=random.randint(100,200) #darkness of the green.
		self.color=rgbString(0, green, 0)

	def draw(self, canvas):
		trunkSize=self.trunkSize
		trunkLenght=self.trunkLength  
		(cx, cy, r)=(self.x, self.y, self.radius)
		canvas.create_rectangle(cx-trunkSize, cy, cx+trunkSize, cy+trunkLenght,
			fill="brown", width=0)
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=self.color, width=0)

class Rock(Obstacle): 
#same effect as mountains, but works with a bound, and see through.

	def __init__(self, x, y):
		super().__init__(x,y)
		self.isTransparent=True
		self.isMovable=False
		self.radius=random.randint(10,17)
		rgb=random.randint(40,100) #Gray has equal rgb.
		self.color=rgbString(rgb,rgb,rgb)
		self.xOffset=random.randint(0,3)
		self.yOffset=random.randint(0,3)

	def draw(self, canvas):
		(cx, cy, r)=(self.x, self.y, self.radius)
		rx=r+self.xOffset
		ry=r+self.yOffset
		canvas.create_oval(cx-rx, cy-ry, cx+rx, cy+ry,
					fill=self.color)


class Hill(Obstacle): #see through, slow movement, strategical advantage.

	def hillInitializer(self):
		x=random.randint(0, self.radius)
		y=random.randint(0, self.radius)
		r=self.radius
		self.hill=(self.x+x,self.y+y,r)

	def __init__(self, x, y):  #hills are composed of semi hills,
		super().__init__(x,y)  #which give them their curvy structure.
		self.isTransparent=True
		self.isMovable=True 
		self.slowDownFactor=0.5
		self.radius=random.randint(50,70)
		self.hillInitializer()

	def draw(self, canvas):
		(cx,cy,r)=self.hill
		(xOffset, yOffset)=(random.randint(-15,15), random.randint(-15,15))
		(rx, ry)=(r+xOffset, r+yOffset) #not perfect circles
		radiusIncrement=2
		(R, G, B, colorIncrement)= (180,90,0, 5) #light Brown
		while r>0:
			if R<=70: R=70
			if G<=35: G=35
			color=rgbString(R, G, B)
			(rx, ry)=(r+xOffset, r+yOffset) #not perfect circles
			canvas.create_oval(cx-rx, cy-ry, cx+rx, cy+ry,
						fill=color, width=0)
			r-=radiusIncrement
			(R, G)=(R-colorIncrement, G-colorIncrement)

#############################################################################
#############################################################################

class Outpost(object):

	def __init__(self, x, y):
		self.x=x
		self.y=y
		self.radius=15 #the color display
		self.OccupationVelocity=0 #plus for blue, minus for red
		self.Occupation=0 #neutral state.
		self.range=100 #the actual range of the outpost.
		self.color=rgbString(0,0,0) #Black
		self.width=0
		self.Occupier=None

	def getColor(self):
		maxOccupation=1000
		maxColor=255
		colorRatio=maxColor/maxOccupation
		if self.Occupation>=0: #Blue occupying.
			blue=round(self.Occupation*colorRatio)
			self.color=rgbString(0,0, blue)
		else: #self.Occupation<0, Red occupying.
			red=round(abs(self.Occupation)*colorRatio)
			self.color=rgbString(red,0,0)

	def contains(self, x, y):
		distance= getDistance((self.x, self.y), (x,y))
		return distance<=self.radius

	def getOccupationVelocity(self, data):
		WarriorsInRange=self.getWarriorsInRange(data)
		for Warrior in WarriorsInRange:
			if Warrior.type=="player": #Blue warrior.
				self.OccupationVelocity+=1
			else: #isinstance(Warrior, Red)
				self.OccupationVelocity-=1

	def getOccupation(self):
		maxOccupation=1000
		self.Occupation+=self.OccupationVelocity
		if self.Occupation>=maxOccupation:
			self.Occupation=maxOccupation
			self.Occupier="blue"
		elif self.Occupation<=-maxOccupation: 
			self.Occupation=-maxOccupation
			self.Occupier="red"

	def getWarriorsInRange(self, data):
		Warriors=[]
		for Warrior in data.Warriors:
			distance=getDistance((self.x, self.y), (Warrior.x, Warrior.y))
			if distance<=self.range: Warriors.append(Warrior)
		return Warriors

	def update(self, data):
		self.OccupationVelocity=0 #reset in each turn.
		self.Occupier=None
		self.getOccupationVelocity(data)
		self.getOccupation()
		self.getColor()

	def draw(self, canvas):
		(cx, cy, r)=(self.x, self.y, self.radius) #inner circle
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=self.color, 
							width=self.width, tags="delete")
		(cx, cy, r)=(self.x, self.y, self.range) #range circle
		canvas.create_oval(cx-r, cy-r, cx+r, cy+r, 
						tags="delete")
		if self.Occupier!=None: #occupation circle.
			(cx, cy, r)=(self.x, self.y, self.radius*2) #inner circle
			canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=self.Occupier, 
					width=10,tags="delete")

