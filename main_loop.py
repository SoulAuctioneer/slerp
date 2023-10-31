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

        # Used to run one-off events in the future
        self.event_scheduler = EventScheduler()

        # Controls the liquid munging hardware
        self.dispenser = Dispenser()

        # Initialize Pygame
        pygame_functions.screenSize(SCREEN_WIDTH, SCREEN_HEIGHT, None, None, IS_FULLSCREEN)
        pygame_functions.setBackgroundImage(BG_IMAGE)  # A background image always sits behind the sprites
        pygame_functions.setAutoUpdate(False)
        self.screen = pygame_functions.screen
        pygame.display.set_caption(WINDOW_CAPTION)

        # Initialize Slerp animation
        self.slerp_sprite = SlerpSprite()

        # Initialize drinkies TODO: Can I get these into settings?
        self.drinks = [
            Drink("INSECURITY ICICLE", (0, 200, 255), (20, 20, 20, 20), self.page_pour_drink1), # cyan
            Drink("JEALOUSY JUICE", (255, 0, 255), (0, 10, 0, 0), self.page_pour_drink2), # magenta
            Drink("JUDGMENTAL JOLT", (255, 200, 0), (0, 0, 10, 0), self.page_pour_drink3), # yellow
            Drink("WRATHFUL WATER", (255, 64, 64), (0, 10, 9, 0), self.page_pour_drink4), # red
            Drink("GREEDY GULP", (0, 255, 64), (8, 0, 10, 0), self.page_pour_drink5), # green
            Drink("MELANCHOLY MASH", (64, 64, 255), (10, 10, 0, 0), self.page_pour_drink6) # blue
        ]
        
    # PAGE: Initial page, sleeping and start button
    def page_start(self):
        self.set_buttons([
            Button(self.screen, pygame.Rect(100, 225, 520, 270), "WAKE UP!", (255, 0, 255), self.page_hello)
        ])
        self.slerp_sprite.start_anim(self.slerp_sprite.animSleeping, 0)
        pygame_functions.makeMusic(random.choice(MUSIC))
        pygame_functions.playMusic()

    # PAGE: Slerp introduces himself
    def page_hello(self):
        self.reset_buttons()
        pygame_functions.stopMusic()
        speech = pygame_functions.makeSound('assets/audio/speechHello.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(20.5, self.show_drink_buttons) # Show drink buttons
        self.event_scheduler.schedule(21.7, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0) # Done talking, switch to resting animation
        self.dispenser.bubble('cyan', 21.7)
        self.dispenser.bubble('magenta', 21.7)
        self.dispenser.bubble('yellow', 21.7)
        self.dispenser.bubble('transparent', 21.7)

    # PAGE: Show drink selection buttons 
    def show_drink_buttons(self):
        buttons = []
        for i, drink in enumerate(self.drinks):
            buttons.append(Button(self.screen, pygame.Rect(50, 50 + i*110, 570, 80), drink.name, drink.rgb, drink.page_function))
        self.set_buttons(buttons)

    # PAGE: Slerp pours a jealousy juice
    def page_pour_drink1(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, self.dispenser.dispense, self.drinks[0])
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)
        self.event_scheduler.schedule(24, self.page_start)

    # PAGE: Slerp pours a jealousy juice
    def page_pour_drink2(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, self.dispenser.dispense, self.drinks[1])
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)
        self.event_scheduler.schedule(24, self.page_start)

    # PAGE: Slerp pours a jealousy juice
    def page_pour_drink3(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, self.dispenser.dispense, self.drinks[2])
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)
        self.event_scheduler.schedule(24, self.page_start)

    # PAGE: Slerp pours a jealousy juice
    def page_pour_drink4(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, self.dispenser.dispense, self.drinks[3])
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)
        self.event_scheduler.schedule(24, self.page_start)

    # PAGE: Slerp pours a jealousy juice
    def page_pour_drink5(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, self.dispenser.dispense, self.drinks[4])
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)
        self.event_scheduler.schedule(24, self.page_start)

    # PAGE: Slerp pours a jealousy juice
    def page_pour_drink6(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, self.dispenser.dispense, self.drinks[5])
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)
        self.event_scheduler.schedule(24, self.page_start)

    def page_admin(self):
        pygame_functions.stopMusic()
        self.set_buttons([
            Button(self.screen, pygame.Rect(50, 25, 570, 70), 'RESTART', (50, 255, 50), self.page_start),
            Button(self.screen, pygame.Rect(50, 110, 570, 70), 'DRINKS SCREEN', (50, 50, 255), self.show_drink_buttons),
            Button(self.screen, pygame.Rect(50, 195, 570, 70), 'TEST CYAN', (0, 255, 255), self.dispenser.test, 'cyan'),
            Button(self.screen, pygame.Rect(50, 280, 570, 70), 'TEST MAGENTA', (255, 0, 255), self.dispenser.test, 'magenta'),
            Button(self.screen, pygame.Rect(50, 365, 570, 70), 'TEST YELLOW', (255, 255, 0), self.dispenser.test, 'yellow'),
            Button(self.screen, pygame.Rect(50, 450, 570, 70), 'TEST TRANSPARENT', (150, 150, 165), self.dispenser.test, 'transparent'),
            Button(self.screen, pygame.Rect(50, 535, 570, 70), 'TEST PRIMING', (180, 128, 128), self.dispenser.test_prime),
            Button(self.screen, pygame.Rect(50, 620, 570, 70), 'EXIT', (255, 50, 50), self.stop_loop)
        ])

    def set_buttons(self, buttons):
        self.reset_buttons()
        self.buttons = buttons
        admin_button = Button(self.screen, pygame.Rect(1260, 700, 20, 20), None, None, self.page_admin)
        self.buttons.append(admin_button)

    def reset_buttons(self):
        admin_button = Button(self.screen, pygame.Rect(1260, 700, 20, 20), None, None, self.page_admin)
        self.buttons = [admin_button]
        pygame_functions.setBackgroundImage(BG_IMAGE)  # A background image always sits behind the sprites

    # Handle pygame events
    def handle_pygame_events(self):
        for event in pygame.event.get():
            # Exit on CTRL-Q or CMD-Q
            if event.type == QUIT:
                self.is_loop_running = False
            # Handle clicks or taps
            if event.type == MOUSEBUTTONDOWN:
                # Check if the touch event occurred within a button's area
                for button in self.buttons:
                    button.trigger_if_clicked(event.pos)

    def stop_loop(self):
        self.is_loop_running = False
            
    # Main loop
    def run(self):
        self.is_loop_running = True
        while self.is_loop_running:

            # Handle any touch/click and quit events
            self.handle_pygame_events()

            # Execute any one-time scheduled events that have come due
            self.event_scheduler.execute_due()

            # Execute any due events in the drink dispenser
            self.dispenser.update()

            # Update any running animation
            self.slerp_sprite.update()

            # Draw any buttons
            for button in self.buttons:
                button.draw()

            # Update the display
            pygame_functions.updateDisplay()

            # Run at 24 fps
            pygame_functions.tick(24)

    # Gracefully shut everything down
    def shut_down(self):
        print('Shutting down')
        pygame.quit()
