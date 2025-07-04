import pygame_functions as pgf

class SlerpSprite:
    def __init__(self):

        self.xPos, self.yPos = 600, 0
        self.activeFrameIndex = 0 # Use to iterate over the sprite list
        self.numLoops = 1 # Number of times to loop the animation. Zero loops forever
        self.numLoopsRemaining = 1 # Number of remaining loops
        self.updateInterval = 300 # Delay between frames, in milliseconds
        self.nextFrameTimer = 0 # Clock to track next frame time
        self.slerp = None # The sprite with images
        self.frameList = [] # List of frames to play in one loop
        self.isAnimating = False # Whether we're currently playing an animation

        import os
        self.spriteDict = {}
        spriteFiles = [f for f in os.listdir("assets/sprites") if f.endswith('.png')]
        for i, spriteFile in enumerate(spriteFiles):
            spriteName = os.path.splitext(spriteFile)[0] # Get the filename without extension
            if i == 0:
                self.slerp = pgf.makeSprite(f"assets/sprites/{spriteFile}")
            else:
                pgf.addSpriteImage(self.slerp, f"assets/sprites/{spriteFile}")
            self.spriteDict[spriteName] = i

        self.animSleeping = {
            'frames': self.make_anim(['sleeping1', 'sleeping2', 'sleeping3']),
            'delay': 1500
        }
        self.animWaking = {
            'frames': self.make_anim(['waking1', 'waking2', 'waking3']),
            'delay': 500
        }
        self.animAngry = { 
            'frames': self.make_anim(['talking_angry1', 'talking_angry2', 'talking_angry3', 'talking_angry4']),
            'delay': 300
        }
        self.animTalking = { 
            'frames': self.make_anim(['talking1', 'talking2', 'talking4']),
            'delay': 300
        }
        self.animIdling = {
            'frames': self.make_anim(['bored1', 'bored2', 'bored3', 'bored4', 'bored8', 'bored7', 'waking1', 'bored8']),
            'delay': 2500
        }
        self.animStraining = {
            'frames': self.make_anim(['straining1', 'straining2', 'straining3', 'straining1', 'straining2', 'straining4']),
            'delay': 350,
        }
        self.animTired = {
            'frames': self.make_anim(['straining7', 'bored7']),
            'delay': 500
        }
        self.animSinging = {
            'frames': self.make_anim(['singing5', 'singing6', 'singing7', 'singing5', 'singing6', 'singing8']),
            'delay': 300
        }


    def make_anim(self, names=[]):
        frames = []
        for name in names:
            frames.append(self.spriteDict[name])
        return frames

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
        total_anim_time = len(self.frameList) * anim['delay'] * (loops if loops > 0 else 1)
        return total_anim_time
    
    def stop_anim(self):
        print("Stopping animation")
        self.isAnimating = False

    def refresh(self):
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
