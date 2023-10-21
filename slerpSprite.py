from pygame_functions import *

class SlerpSprite:
    def __init__(self):
        self.animTalking = [0, 1, 0, 1, 0, 1, 0, 1, 2]
        self.animSleeping = [2,3]
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
        self.slerp = makeSprite("assets/sprites/1.png")
        addSpriteImage(self.slerp, "assets/sprites/2.png")
        addSpriteImage(self.slerp, "assets/sprites/3.png")
        addSpriteImage(self.slerp, "assets/sprites/4.png")

    def startAnim(self, frames=[0], loops=0, delay=300):
        self.numLoops = loops
        self.numLoopsRemaining = loops
        self.updateInterval = delay
        self.activeFrameIndex = frames[0]
        self.frameList = frames
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
