from pygame_functions import *

class SlerpSprite:
    def __init__(self):

        self.animTalking = { 
            'frames': [1, 2, 1, 2, 1, 2, 1, 2, 3],
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

        self.xPos, self.yPos = 580, 50
        self.activeFrameIndex = 0 # Use to iterate over the sprite list
        self.numLoops = 1 # Number of times to loop the animation. Zero loops forever
        self.numLoopsRemaining = 1 # Number of remaining loops
        self.updateInterval = 300 # Delay between frames, in milliseconds
        self.nextFrameTimer = 0 # Clock to track next frame time
        self.slerp = None # The sprite with images
        self.frameList = [] # List of frames to play in one loop
        self.isAnimating = False # Whether we're currently playing an animation

    def init(self):
        self.slerp = makeSprite("assets/sprites/0.png")
        addSpriteImage(self.slerp, "assets/sprites/1.png")
        addSpriteImage(self.slerp, "assets/sprites/2.png")
        addSpriteImage(self.slerp, "assets/sprites/3.png")
        addSpriteImage(self.slerp, "assets/sprites/4.png")

    def startAnim(self, anim, loops=0):
        self.numLoops = loops
        self.numLoopsRemaining = loops
        self.updateInterval = anim['delay']
        self.frameList = anim['frames']
        self.activeFrameIndex = self.frameList[0]
        changeSpriteImage(self.slerp, self.activeFrameIndex)
        moveSprite(self.slerp, self.xPos, self.yPos)
        showSprite(self.slerp)
        self.nextFrameTimer = clock()
        self.isAnimating = True
    
    def stopAnim(self):
        print("Stopping animation")
        self.isAnimating = False

    def updateAnim(self):
        if clock() > self.nextFrameTimer and self.isAnimating:
            if (self.activeFrameIndex + 1 < len(self.frameList)):
                self.activeFrameIndex += 1
                changeSpriteImage(self.slerp, self.frameList[self.activeFrameIndex])
            else:
                if self.numLoopsRemaining > 0 or self.numLoops == 0:
                    self.activeFrameIndex = 0
                    changeSpriteImage(self.slerp, self.frameList[self.activeFrameIndex])
                if self.numLoops > 0:
                    self.numLoopsRemaining -= 1
            self.nextFrameTimer = clock() + self.updateInterval
