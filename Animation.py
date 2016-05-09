#Adapted from class notes.

from tkinter import *

class Animation(object):

    def mousePressed(self, event): pass
    def mouseMoved(self, event): pass
    def mouseReleased(self, event): pass
    def shiftMousePressed(self, event): pass
    def keyPressed(self, event): pass
    def timerFired(self): pass
    def init(self):
        self.width=1200
        self.height=600
    def redrawAll(self): pass
    def shiftMouseMoved(self, event): pass
    #for the menus: tutorial and campaign.
    def drawModelWarrior(self, canvas, cx, cy, r, color):
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color)
        #also draw the head.
        canvas.create_line((cx,cy), (cx,cy-r), width=3)

    def run(self, width=300, height=300):
        # create the root and the canvas
        root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()

        # set up events
        def redrawAllWrapper():
            self.canvas.delete("delete") #deletes only the canvas draws with
            self.redrawAll()            #the parameter delete. Efficiency!
            self.canvas.update()        #i.e doesn't delete/redraw the
                                                                #background.
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()

        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()

        def mouseMovedWrapper(event):
            self.mouseMoved(event)
            #Don't call redrawAll at each mouseMoved. Slows it down.

        def mouseReleasedWrapper(event):
            self.mouseReleased(event)
            redrawAllWrapper()

        def shiftMousePressedWrapper(event):
            self.shiftMousePressed(event)
            redrawAllWrapper()

        def shiftMouseMovedWrapper(event):
            self.shiftMouseMoved(event)

        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<Shift-Button-1>", shiftMousePressedWrapper)
        root.bind("<Shift-B1-Motion>", shiftMouseMovedWrapper)
        root.bind("<Key>", keyPressedWrapper)
        root.bind("<B1-Motion>", mouseMovedWrapper)
        root.bind("<B1-ButtonRelease>", mouseReleasedWrapper)

        # set up timerFired events
        self.timerFiredDelay = 20 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)

        # init and get timerFired running
        self.init()
        timerFiredWrapper()
        # and launch the app
        root.mainloop()
        print("Bye")
