import sys
import pygame
from pygame.locals import *
import button
import dispenser
import pygame_functions
import EventScheduler
from slerpSprite import SlerpSprite

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT, IS_FULLSCREEN = 1280, 720, True

# Background image
BG_IMAGE = "assets/background-logo-1280x720.png"

# The pygame screen surface
screen = None

# Buttons currently onscreen
buttons = []

# Slerp animations
slerpSprite = None

# Hidden quit button. TODO: Send user to a menu instead, with quit, resume and reset
quitButtonRect = pygame.Rect(1260, 700, 20, 20)

eventScheduler = EventScheduler.EventScheduler()

# PAGE: Initial page, sleeping and start button
def pageStart():

    global buttons
    buttons = [
        {
            "string": "WAKE UP!",
            "background": (255, 0, 255),
            "rect": pygame.Rect(100, 225, 520, 270),
            "func": pageHello
        }
    ]
    slerpSprite.startAnim(slerpSprite.animSleeping, 0)
    pygame_functions.makeMusic('assets/audio/music.mp3')
    pygame_functions.playMusic()

# PAGE: Slerp introduces himself
def pageHello():
    resetButtons()
    pygame_functions.stopMusic()
    speech = pygame_functions.makeSound('assets/audio/speechHello.mp3')
    pygame_functions.playSound(speech)
    slerpSprite.startAnim(slerpSprite.animTalking, 0)
    eventScheduler.schedule(20.5, pageDrinks1) # Show drink buttons
    eventScheduler.schedule(21.7, lambda: slerpSprite.startAnim(slerpSprite.animResting, 0)) # Done talking, switch to resting animation

# PAGE: Slerp pours a jealousy juice
def pagePourDrinkJealousyJuice():
    resetButtons()
    speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
    pygame_functions.playSound(speech)
    slerpSprite.startAnim(slerpSprite.animTalking, 0)
    eventScheduler.schedule(5, lambda: dispenser.dispense('drink1'))
    eventScheduler.schedule(18, lambda: slerpSprite.startAnim(slerpSprite.animResting, 0))
    eventScheduler.schedule(24, pageStart)

# PAGE: Show drink selection buttons # TODO better to be a const set within pageHello()
def pageDrinks1():
    global buttons
    # Define the button positions, sizes, labels, actions, animations
    buttons = [
        {
            "string": "INSECURITY ICICLE",
            "background": (128, 0, 255),
            "rect": pygame.Rect(50, 50, 570, 80),
            "func": pagePourDrinkJealousyJuice,
        },
        {
            "string": "JEALOUSY JUICE",
            "background": (255, 0, 255),
            "rect": pygame.Rect(50, 160, 570, 80),
            "func": pagePourDrinkJealousyJuice,
        },
        {
            "string": "WRATHFUL WATER",
            "background": (255, 64, 64),
            "rect": pygame.Rect(50, 270, 570, 80),
            "func": pagePourDrinkJealousyJuice,
        },
        {
            "string": "JUDGMENTAL JOLT",
            "background": (255, 200, 0),
            "rect": pygame.Rect(50, 380, 570, 80),
            "func": pagePourDrinkJealousyJuice,
        },
        {
            "string": "GREEDY GULP",
            "background": (0, 255, 64),
            "rect": pygame.Rect(50, 490, 570, 80),
            "func": pagePourDrinkJealousyJuice,
        },
        {
            "string": "MELANCHOLY MASH",
            "background": (64, 64, 255),
            "rect": pygame.Rect(50, 600, 570, 80),
            "func": pagePourDrinkJealousyJuice,
        },
    ]

# Handle pygame events
def handlePyEvents():
    global isLoopRunning
    for event in pygame.event.get():

        # Exit on CTRL-Q or CMD-Q
        if event.type == QUIT:
            isLoopRunning = False

        # Handle clicks or taps
        if event.type == MOUSEBUTTONDOWN:
            # Check if the touch event occurred within a button's area
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quitButtonRect.collidepoint(event.pos):
                    isLoopRunning = False
                for buttonDef in buttons:
                    if buttonDef['rect'].collidepoint(event.pos):
                        buttonDef['func']()

def resetButtons():
    global buttons
    buttons = []
    pygame_functions.setBackgroundImage(BG_IMAGE)  # A background image always sits behind the sprites

# Initialize all the good stuff
def init():
    global screen, slerpSprite

    # Initialize drink dispenser
    dispenser.init()

    # Initialize Pygame
    pygame_functions.screenSize(SCREEN_WIDTH, SCREEN_HEIGHT, None, None, IS_FULLSCREEN)
    pygame_functions.setBackgroundImage(BG_IMAGE)  # A background image always sits behind the sprites
    pygame_functions.setAutoUpdate(False)
    screen = pygame_functions.screen
    pygame.display.set_caption('Slerp the Slushmaster')

    # Initialize Slerp animation
    slerpSprite = SlerpSprite()
    slerpSprite.init()

# Gracefully shut everything down and exit
def shutDown():
    print('Shutting down')
    dispenser.shutDown()
    pygame.quit()
    sys.exit()

# Main loop
def main():
    global isLoopRunning
    isLoopRunning = True
    while isLoopRunning:

        # Handle any touch/click and quit events
        handlePyEvents()

        # Execute any one-time scheduled events that have come due
        eventScheduler.executeDue()

        # Update any running animation
        slerpSprite.updateAnim()

        # Draw any buttons
        for buttonDef in buttons:
            button.draw_button(screen, buttonDef['rect'], buttonDef['string'], buttonDef['background'])

        # Update the display
        pygame_functions.updateDisplay()

        # Run at 24fps
        pygame_functions.tick(24)

    # Shut down
    shutDown()

if __name__ == "__main__":
    # Initialize all the good stuff
    init()
    # Fire up the first page of the narrative
    pageStart()
    # Start the main loop
    main()
