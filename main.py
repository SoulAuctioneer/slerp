import sys
import pygame
from pygame.locals import *
from button import Button
from dispenser import Dispenser
import pygame_functions
from event_scheduler import EventScheduler
from slerpSprite import SlerpSprite
from settings import *

class MainLoop:
    def __init__(self):

        # Buttons currently onscreen
        self.buttons = []

        # Hidden quit button. TODO: Send user to a menu instead, with quit, resume and reset
        self.quitButtonRect = pygame.Rect(1260, 700, 20, 20)

        # Used to run one-off events in the future
        self.eventScheduler = EventScheduler()

        # Controls the liquid munging hardware
        self.dispenser = Dispenser()

        # Initialize Pygame
        pygame_functions.screenSize(SCREEN_WIDTH, SCREEN_HEIGHT, None, None, IS_FULLSCREEN)
        pygame_functions.setBackgroundImage(BG_IMAGE)  # A background image always sits behind the sprites
        pygame_functions.setAutoUpdate(False)
        self.screen = pygame_functions.screen
        pygame.display.set_caption(WINDOW_CAPTION)

        # Initialize Slerp animation
        self.slerpSprite = SlerpSprite()

    # PAGE: Initial page, sleeping and start button
    def pageStart(self):
        self.buttons = [
            Button(self.screen, pygame.Rect(100, 225, 520, 270), "WAKE UP!", (255, 0, 255), self.pageHello)
        ]
        self.slerpSprite.startAnim(self.slerpSprite.animSleeping, 0)
        pygame_functions.makeMusic('assets/audio/music.mp3')
        pygame_functions.playMusic()

    # PAGE: Slerp introduces himself
    def pageHello(self):
        self.resetButtons()
        pygame_functions.stopMusic()
        speech = pygame_functions.makeSound('assets/audio/speechHello.mp3')
        pygame_functions.playSound(speech)
        self.slerpSprite.startAnim(self.slerpSprite.animTalking, 0)
        self.eventScheduler.schedule(20.5, self.pageDrinks1) # Show drink buttons
        self.eventScheduler.schedule(21.7, lambda: self.slerpSprite.startAnim(self.slerpSprite.animResting, 0)) # Done talking, switch to resting animation

    # PAGE: Show drink selection buttons # TODO better to be a const set within pageHello()
    def pageDrinks1(self):
        # Define the button positions, sizes, labels, actions, animations
        self.buttons = [
            Button(self.screen, pygame.Rect(50, 50, 570, 80), "INSECURITY ICICLE", (128, 0, 255), self.pagePourDrinkJealousyJuice),
            Button(self.screen, pygame.Rect(50, 160, 570, 80), "JEALOUSY JUICE", (255, 0, 255), self.pagePourDrinkJealousyJuice),
            Button(self.screen, pygame.Rect(50, 270, 570, 80), "WRATHFUL WATER", (255, 64, 64), self.pagePourDrinkJealousyJuice),
            Button(self.screen, pygame.Rect(50, 380, 570, 80), "JUDGMENTAL JOLT", (255, 200, 0), self.pagePourDrinkJealousyJuice),
            Button(self.screen, pygame.Rect(50, 490, 570, 80), "GREEDY GULP", (0, 255, 64), self.pagePourDrinkJealousyJuice),
            Button(self.screen, pygame.Rect(50, 600, 570, 80), "MELANCHOLY MASH", (64, 64, 255), self.pagePourDrinkJealousyJuice),
        ]

    # PAGE: Slerp pours a jealousy juice
    def pagePourDrinkJealousyJuice(self):
        self.resetButtons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerpSprite.startAnim(self.slerpSprite.animTalking, 0)
        self.eventScheduler.schedule(5, lambda: self.dispenser.dispense('drink1'))
        self.eventScheduler.schedule(18, lambda: self.slerpSprite.startAnim(self.slerpSprite.animResting, 0))
        self.eventScheduler.schedule(24, self.pageStart)

    # Handle pygame events
    def handlePyEvents(self):
        for event in pygame.event.get():

            # Exit on CTRL-Q or CMD-Q
            if event.type == QUIT:
                self.isLoopRunning = False

            # Handle clicks or taps
            if event.type == MOUSEBUTTONDOWN:
                # Check if the touch event occurred within a button's area
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.quitButtonRect.collidepoint(event.pos):
                        self.isLoopRunning = False
                    for button in self.buttons:
                        if button.rect.collidepoint(event.pos):
                            button.on_click()

    def resetButtons(self):
        self.buttons = []
        pygame_functions.setBackgroundImage(BG_IMAGE)  # A background image always sits behind the sprites

    # Main loop
    def run(self):
        self.isLoopRunning = True
        while self.isLoopRunning:

            # Handle any touch/click and quit events
            self.handlePyEvents()

            # Execute any one-time scheduled events that have come due
            self.eventScheduler.execute_due()

            # Execute any due events in the drink dispenser
            self.dispenser.update()

            # Update any running animation
            self.slerpSprite.updateAnim()

            # Draw any buttons
            for button in self.buttons:
                button.draw()

            # Update the display
            pygame_functions.updateDisplay()

            # Run at 24fps
            pygame_functions.tick(24)

    # Gracefully shut everything down
    def shutDown(self):
        print('Shutting down')
        pygame.quit()

if __name__ == "__main__":

    # Initialize the looper
    main_loop = MainLoop()

    # Fire up the first page of the narrative
    main_loop.pageStart()

    # Start the main loop running
    main_loop.run()

    # Quit, so shut down the main loop
    main_loop.shutDown()
