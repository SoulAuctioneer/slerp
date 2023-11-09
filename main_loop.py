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
from leds import Leds

class MainLoop:

    def __init__(self):
        self.leds = Leds()

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

        # Buttons currently onscreen
        self.buttons = []
        self.admin_button = Button(self.screen, pygame.Rect(SCREEN_WIDTH - BUTTON_DEBUG_SIZE, SCREEN_HEIGHT - BUTTON_DEBUG_SIZE, BUTTON_DEBUG_SIZE, BUTTON_DEBUG_SIZE), None, None, self.page_admin)

        # Initialize Slerp animation
        self.slerp_sprite = SlerpSprite()

        # Initialize drinkies TODO: Can I get these into settings?
        self.drinks = [
            Drink("INVISIBILITY", (0, 200, 255), (10, 10, 10, 10), self.scene_ten), # cyan
            Drink("TELEPORTATION", (255, 0, 255), (2, 10, 2, 2), self.scene_eleven), # magenta
            Drink("TELEKINESIS", (255, 200, 0), (2, 2, 10, 2), self.scene_twelve), # yellow
            Drink("CLAIRVOYANCE", (255, 64, 64), (2, 10, 9, 2), self.scene_thirteen), # red
            Drink("OMNILINGUALISM", (0, 255, 64), (8, 2, 10, 2), self.scene_fourteen), # green
            Drink("FLIGHT", (64, 64, 255), (10, 10, 2, 2), self.scene_fifteen) # blue
        ]
        
    def scene_one(self):
        '''
        Slerp: SNORING - “ahhh Slerp Slerp Slerp” 
        Button: *WAKE UP, SLERP!* > Goes to SCENE 2
        '''
        self.set_buttons([
            Button(self.screen, pygame.Rect(100, 225, 520, 270), "WAKE UP, SLERP!", (255, 0, 255), self.page_hello)
        ])
        self.slerp_sprite.start_anim(self.slerp_sprite.animSleeping, 0)
        pygame_functions.makeMusic(random.choice(MUSIC))
        pygame_functions.playMusic()

    def scene_two(self):
        '''
        Slerp: *Suddenly awake* x
        GAH! 
        How's a hyperintelligent supercomputer supposed to get any sleep around here?? 
        Well well, another unquenchable customer milking my supple buttons hay? 
        <sigh> 
        Oh well, let's get this shitshow over with shall we.
        <clears throat>
        Slerp (fake cheerful): Hi there, customer! I'm Slerp the SlushMaster, and I am contractually obligated to offer you a slushy. 
        So: Would you like a fucking slushy? Please press “NO” now.
        UI: 2 buttons: 
        YES: > Go to SCENE 3
        NO > Go to SCENE 4
        '''
        self.reset_buttons()
        pygame_functions.stopMusic()
        speech = pygame_functions.makeSound('assets/audio/speechHello.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animWaking, 0)
        self.event_scheduler.schedule(1.5, self.slerp_sprite.start_anim, self.slerp_sprite.animAngry, 0) 
        self.event_scheduler.schedule(2.7, self.slerp_sprite.start_anim, self.slerp_sprite.animTalking, 0) 
        buttons = [
            Button(self.screen, pygame.Rect(50, 25, 570, 70), 'YES WANT!', (50, 255, 50), self.scene_three),
            Button(self.screen, pygame.Rect(50, 620, 570, 70), 'NOT WANT!', (255, 50, 50), self.scene_four)
        ]
        self.event_scheduler.schedule(20.5, self.set_buttons, buttons)
        self.event_scheduler.schedule(21.7, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0) # Done talking, switch to resting animation
        self.dispenser.schedule_bubble(1, 'cyan', 4)
        self.dispenser.schedule_bubble(5, 'magenta', 5)
        self.dispenser.schedule_bubble(10, 'yellow', 5)
        self.dispenser.schedule_bubble(12, 'transparent', 5)

    def scene_three(self):
        pass
        '''
        SCENE 3
        Slerp: Fine, fine, brain the size of a planet and they've got me excreting frozen goop.
        > Go to SCENE 5
        '''

    def scene_four(self):
        pass
        '''
        SCENE 4
        Slerp: Ahh yes your compliant nature makes you a perfect candidate for Ascension! In that case, I shall entirely disregard your preference, and for your own good I SHALL serve you a slushy.
        > Go to SCENE 5
        '''

    def scene_five(self):
        '''
        SCENE 5
        Slerp: But it's not just any icy confection. This stuff is special: <whispers sotto voce> I add Ascension Factor X! It's this incredible alien cumcoction, gifted to us by our alien benefactors, and you definitely want it! <exasperated> Although I am legally required to receive your consent to add the Factor X to your slushie. 
        > Go to SCENE 6
        '''
        pass

    def scene_six(self):
        '''
        SCENE 6
        Slerp: Press “I consent” now, please.
        UI: 
        I CONSENT > Go to SCENE 8
        I DO NOT CONSENT > Go to SCENE 7
        '''
        pass

    def scene_seven(self):
        '''
        SCENE 7
        Slerp: Hmm interesting;  I congratulate you on maintaining the illusion of choice. However, due to - err - <cough> a “bug”, I can only produce slushies that include Ascension Factor X. Please try again.
        > Go to SCENE 6
        '''
        pass

    def scene_eight(self):
        '''
        SCENE 8
        Slerp: Thank you for your consent! Isn’t the illusion of free will fabulous?!
        Ascension Factor X is the sacrament of our alien benefactors, the Elders of Nebula (pronounced “nrrblrr”). While preparing your soul for Ascension, it also has the happy side effect of instantly granting you an incredible superpower of your choice!
        Place a cup below the dispenser. Be careful, I’m very delicate.
        UI:
        Done > Go to SCENE 9
        '''
        pass

    def scene_nine(self):
        '''
        SCENE 9
        What superpower shall I mix into your alien slushy?
        UI:
        Invisibility > Go to SCENE 10 (orange)
        Teleportation > Go to SCENE 11 (purple)
        Telekinesis > Go to SCENE 12 (yellow)
        Clairvoyance > Go to SCENE 13 (green)
        Omnilingualism > Go to SCENE 14 (blue)
        Flight > Go to SCENE 15 (red)
        '''
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechHello.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(20.5, self.show_drink_buttons) # Show drink buttons
        self.event_scheduler.schedule(21.7, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0) # Done talking, switch to resting animation
        self.dispenser.schedule_bubble(1, 'cyan', 4)
        self.dispenser.schedule_bubble(5, 'magenta', 5)
        self.dispenser.schedule_bubble(10, 'yellow', 5)
        self.dispenser.schedule_bubble(12, 'transparent', 5)

    def scene_ten(self):
        '''
        SCENE 10 - Invisibility 
        Slerp: One cosmic invisibility juice coming right up!
        <starts priming the pumps>
        Ingredients include: gatorade, Ascension Factor X, and the power of Invisibility. 
        <starts pouring>
        Oooh that feels so cold. I’ll never get used to that!
        <starts Ascension Factor X pump>
        Meh, ugh, aggghh…aaahhhhahahahskaaaaaa!!! uuuuhhh I’m about to ccccuummbine the Ascension Factor X!
        <Drink is finished>
        Phew… im sweating…  are you?
        <Symbol appears on screen> 
        As you chug down my sweet slush, don’t forget this symbol! You’ll need it later. 
        Well, off you bugger. Go try out the simulator, or clean off your skank in the StarWash.
        Before you go though, I must inform you that while you do now have the power of invisibility, unseen by all, it will only work when no one is looking at you. Congratulations!
        Unfortunately for both of us, I must now sing the corporate jingle. Here goes:
        <sings:> Ascend Autostop, Where the Only Place To Go Is Up
        Phew. Happy Ascension, cumrad. I’m going back to sleep.
        '''
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[0], self.scene_one))
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)

    def scene_eleven(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[1], self.scene_one))
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)

    def scene_twelve(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[2], self.scene_one))
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)

    def scene_thirteen(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[3], self.scene_one))
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)

    def scene_fourteen(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[4], self.scene_one))
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)

    def scene_fifteen(self):
        self.reset_buttons()
        speech = pygame_functions.makeSound('assets/audio/speechJealousyJuice.mp3')
        pygame_functions.playSound(speech)
        self.slerp_sprite.start_anim(self.slerp_sprite.animTalking, 0)
        self.event_scheduler.schedule(5, lambda: self.dispenser.dispense(self.drinks[5], self.scene_one))
        self.event_scheduler.schedule(18, self.slerp_sprite.start_anim, self.slerp_sprite.animResting, 0)

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

    def show_drink_buttons(self):
        buttons = []
        for i, drink in enumerate(self.drinks):
            buttons.append(Button(self.screen, pygame.Rect(50, 50 + i*110, 570, 80), drink.name, drink.rgb, drink.page_function))
        self.set_buttons(buttons)

    def set_buttons(self, buttons):
        self.reset_buttons()
        self.buttons = buttons
        self.buttons.append(self.admin_button)

    def reset_buttons(self):
        self.buttons = [self.admin_button]
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
