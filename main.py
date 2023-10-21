import sys
import time

import pygame
import serial
from pygame.locals import *
import cv2
import COMPorts
import button
import pygame_functions
from slerpSprite import SlerpSprite
from threading import Timer

# TODO: Check if this can change across OS
SERIAL_PORT_DESC = 'IOUSBHostDevice'

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT, IS_FULLSCREEN = 1280, 720, True

# Background image
BG_IMAGE = "assets/background-logo-1280x720.png"

# The Arduino port
arduino = None

# The pygame screen surface
screen = None

# Buttons currently onscreen
buttons = []

slerpSprite = None

def pageStart():
    global buttons
    buttons = [
        {
            "string": "WAKE UP!",
            "background": (255, 0, 255),
            "rect": pygame.Rect(100, 225, 520, 270),
            "func": pageHello,
            "arduino_cmd": b'CMD_DRINK1'
        }
    ]
    slerpSprite.startAnim(slerpSprite.animSleeping, 0)
    pygame_functions.makeMusic('assets/audio/music.mp3')
    pygame_functions.playMusic()

def pageHello():
    resetButtons()
    pygame_functions.stopMusic()
    speech = pygame_functions.makeSound('assets/audio/speechHello.mp3')
    pygame_functions.playSound(speech)
    slerpSprite.startAnim(slerpSprite.animTalking, 0)
    Timer(20.5, pageDrinks1).start() # Show drink buttons
    Timer(21.7, lambda: slerpSprite.startAnim(slerpSprite.animResting, 0)).start() # Done talking, switch to resting animation

# Define narrative functions
def pagePourDrinkJealousyJuice():
    resetButtons()
    speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
    pygame_functions.playSound(speech)
    slerpSprite.startAnim(slerpSprite.animTalking, 0)
    Timer(18, lambda: slerpSprite.startAnim(slerpSprite.animResting, 0)).start()
    Timer(23, pageStart).start()

def pageDrinks1():
    global buttons
    # Define the button positions, sizes, labels, actions, animations, and Arduino commands
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


def resetButtons():
    global buttons
    buttons = []
    pygame_functions.setBackgroundImage(BG_IMAGE)  # A background image always sits behind the sprites

def init():
    global arduino, screen, slerpSprite

    # Initialize Arduino communication
    print('Initializing Arduino communication')
    port_name = COMPorts.get_device_by_description(SERIAL_PORT_DESC)
    print(port_name)
    arduino = serial.Serial(port=port_name, baudrate=9600, timeout=5)
    time.sleep(1)  # Seems like it needs a moment before you can start sending commands

    # Initialize Pygame
    pygame_functions.screenSize(SCREEN_WIDTH, SCREEN_HEIGHT, None, None, IS_FULLSCREEN)
    pygame_functions.setBackgroundImage(BG_IMAGE)  # A background image always sits behind the sprites
    pygame_functions.setAutoUpdate(False)
    screen = pygame_functions.screen
    pygame.display.set_caption('Slerp the Slushmaster')

    # Initialize Slerp animation
    slerpSprite = SlerpSprite()
    slerpSprite.init()

def main():

    init()

    # Fire up the first page of the narrative
    pageStart()

    quitButtonRect = pygame.Rect(1260, 700, 20, 20)

    # Event handling loop
    playing_video = None
    running = True
    while running:

        # Handle events
        for event in pygame.event.get():

            # Exit on CTRL-Q or CMD-Q
            if event.type == QUIT:
                running = False

            # Handle clicks or taps
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button (touchscreen)
                    touch_pos = pygame.mouse.get_pos()  # Get touchscreen position
                    x, y = touch_pos

                    # Check if the touch event occurred within a button's area
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if quitButtonRect.collidepoint(event.pos):
                            running = False
                        else:
                            for buttonDef in buttons:
                                if buttonDef['rect'].collidepoint(event.pos):
                                    print(f"{buttonDef['string']} was pressed!")
                                    buttonDef['func']()

        # Update any running animation
        slerpSprite.updateAnim()

        # Draw any buttons
        for buttonDef in buttons:
            button.draw_button(screen, buttonDef['rect'], buttonDef['string'], buttonDef['background'])

        # Update the display
        pygame_functions.updateDisplay()

        # Run at 60fps (trying 120 -- touchscreen's not very responsive at 60)
        pygame_functions.tick(60)

    # Shut down
    print('Shutting down')
    arduino.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
