import pygame_functions as pgf

class SlerpSprite:
    def __init__(self):

        self.slerp = pgf.makeSprite("assets/sprites/0.png")
        pgf.addSpriteImage(self.slerp, "assets/sprites/1.png")
        pgf.addSpriteImage(self.slerp, "assets/sprites/2.png")
        pgf.addSpriteImage(self.slerp, "assets/sprites/3.png")
        pgf.addSpriteImage(self.slerp, "assets/sprites/4.png")

        self.animTalking = { 
            'frames': [2, 1, 2, 1, 2, 1, 2, 1, 3, 1],
            'delay': 300
        }
        self.animSleeping = {
            'frames': [3, 4],
            'delay': 1500
        }
        self.animResting = {
            'frames': [1, 0],
            'delay': 3000
        }

        self.xPos, self.yPos = 700, 30
        self.activeFrameIndex = 0 # Use to iterate over the sprite list
        self.numLoops = 1 # Number of times to loop the animation. Zero loops forever
        self.numLoopsRemaining = 1 # Number of remaining loops
        self.updateInterval = 300 # Delay between frames, in milliseconds
        self.nextFrameTimer = 0 # Clock to track next frame time
        self.slerp = None # The sprite with images
        self.frameList = [] # List of frames to play in one loop
        self.isAnimating = False # Whether we're currently playing an animation

    def start_anim(self, anim, loops=0):
        self.numLoops = loops
        self.numLoopsRemaining = loops
        self.updateInterval = anim['delay']
        self.frameList = anim['frames']
        self.activeFrameIndex = self.frameList[0]
        pgf.changeSpriteImage(self.slerp, self.activeFrameIndex)
        pgf.moveSprite(self.slerp, self.xPos, self.yPos)
        pgf.showSprite(self.slerp)
        self.nextFrameTimer = pgf.clock()
        self.isAnimating = True
    
    def stop_anim(self):
        print("Stopping animation")
        self.isAnimating = False

    def update(self):
        if pgf.clock() > self.nextFrameTimer and self.isAnimating:
            if (self.activeFrameIndex + 1 < len(self.frameList)):
                self.activeFrameIndex += 1
                pgf.changeSpriteImage(self.slerp, self.frameList[self.activeFrameIndex])
            else:
                if self.numLoopsRemaining > 0 or self.numLoops == 0:
                    self.activeFrameIndex = 0
                    pgf.changeSpriteImage(self.slerp, self.frameList[self.activeFrameIndex])
                if self.numLoops > 0:
                    self.numLoopsRemaining -= 1
            self.nextFrameTimer = pgf.clock() + self.updateInterval
