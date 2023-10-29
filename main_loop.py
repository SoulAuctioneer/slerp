import pygame
from drink import Drink
import pygame_functions
import random
from pygame.locals import *
from button import Button
from dispenser import Dispenser
from event_scheduler import EventScheduler
from slerp_sprite import SlerpSprite
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

        # Initialize drinkies TODO: Can I get these into settings?
        self.drinks = [
            Drink("INSECURITY ICICLE", (0, 200, 255), (10, 0, 0, 0), self.pagePourDrink1), # cyan
            Drink("JEALOUSY JUICE", (255, 0, 255), (0, 10, 0, 0), self.pagePourDrink2), # magenta
            Drink("JUDGMENTAL JOLT", (255, 200, 0), (0, 0, 10, 0), self.pagePourDrink4), # yellow
            Drink("WRATHFUL WATER", (255, 64, 64), (0, 10, 10, 0), self.pagePourDrink3), # red
            Drink("GREEDY GULP", (0, 255, 64), (10, 0, 10, 0), self.pagePourDrink5), # green
            Drink("MELANCHOLY MASH", (64, 64, 255), (10, 10, 0, 0), self.pagePourDrink6) # blue
        ]
        
    # PAGE: Initial page, sleeping and start button
    def pageStart(self):
        self.buttons = [
            Button(self.screen, pygame.Rect(100, 225, 520, 270), "WAKE UP!", (255, 0, 255), self.pageHello)
        ]
        self.slerpSprite.start_anim(self.slerpSprite.animSleeping, 0)
        pygame_functions.makeMusic(random.choice(MUSIC))
        pygame_functions.playMusic()

    # PAGE: Slerp introduces himself
    def pageHello(self):
        self.resetButtons()
        pygame_functions.stopMusic()
        speech = pygame_functions.makeSound('assets/audio/speechHello.mp3')
        pygame_functions.playSound(speech)
        self.slerpSprite.start_anim(self.slerpSprite.animTalking, 0)
        self.eventScheduler.schedule(20.5, self.pageDrinks1) # Show drink buttons
        self.eventScheduler.schedule(21.7, lambda: self.slerpSprite.start_anim(self.slerpSprite.animResting, 0)) # Done talking, switch to resting animation

    # PAGE: Show drink selection buttons # TODO better to be a const set within pageHello()
    def pageDrinks1(self):
        # Define the button positions, sizes, labels, actions, animations
        self.buttons = []
        for i, drink in enumerate(self.drinks):
            self.buttons.append(Button(self.screen, pygame.Rect(50, 50 + i*110, 570, 80), drink.name, drink.rgb, drink.page_function))

    # PAGE: Slerp pours a jealousy juice
    def pagePourDrink1(self):
        self.resetButtons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerpSprite.start_anim(self.slerpSprite.animTalking, 0)
        self.eventScheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[0]))
        self.eventScheduler.schedule(18, lambda: self.slerpSprite.start_anim(self.slerpSprite.animResting, 0))
        self.eventScheduler.schedule(24, self.pageStart)

    # PAGE: Slerp pours a jealousy juice
    def pagePourDrink2(self):
        self.resetButtons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerpSprite.start_anim(self.slerpSprite.animTalking, 0)
        self.eventScheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[1]))
        self.eventScheduler.schedule(18, lambda: self.slerpSprite.start_anim(self.slerpSprite.animResting, 0))
        self.eventScheduler.schedule(24, self.pageStart)

    # PAGE: Slerp pours a jealousy juice
    def pagePourDrink3(self):
        self.resetButtons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerpSprite.start_anim(self.slerpSprite.animTalking, 0)
        self.eventScheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[2]))
        self.eventScheduler.schedule(18, lambda: self.slerpSprite.start_anim(self.slerpSprite.animResting, 0))
        self.eventScheduler.schedule(24, self.pageStart)

    # PAGE: Slerp pours a jealousy juice
    def pagePourDrink4(self):
        self.resetButtons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerpSprite.start_anim(self.slerpSprite.animTalking, 0)
        self.eventScheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[3]))
        self.eventScheduler.schedule(18, lambda: self.slerpSprite.start_anim(self.slerpSprite.animResting, 0))
        self.eventScheduler.schedule(24, self.pageStart)

    # PAGE: Slerp pours a jealousy juice
    def pagePourDrink5(self):
        self.resetButtons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerpSprite.start_anim(self.slerpSprite.animTalking, 0)
        self.eventScheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[4]))
        self.eventScheduler.schedule(18, lambda: self.slerpSprite.start_anim(self.slerpSprite.animResting, 0))
        self.eventScheduler.schedule(24, self.pageStart)

    # PAGE: Slerp pours a jealousy juice
    def pagePourDrink6(self):
        self.resetButtons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerpSprite.start_anim(self.slerpSprite.animTalking, 0)
        self.eventScheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[5]))
        self.eventScheduler.schedule(18, lambda: self.slerpSprite.start_anim(self.slerpSprite.animResting, 0))
        self.eventScheduler.schedule(24, self.pageStart)

    # Handle pygame events
    def handle_pygame_events(self):
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
            self.handle_pygame_events()

            # Execute any one-time scheduled events that have come due
            self.eventScheduler.execute_due()

            # Execute any due events in the drink dispenser
            self.dispenser.update()

            # Update any running animation
            self.slerpSprite.update()

            # Draw any buttons
            for button in self.buttons:
                button.draw()

            # Update the display
            pygame_functions.updateDisplay()

            # Run at 24fps
            pygame_functions.tick(24)

    # Gracefully shut everything down
    def shut_down(self):
        print('Shutting down')
        pygame.quit()
