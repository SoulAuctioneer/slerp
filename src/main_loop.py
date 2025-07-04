import pygame
from .drink import Drink
import pygame_functions
import random
from pygame.locals import *
from .button import Button
from .dispenser import Dispenser
from .event_scheduler import EventScheduler
from .audio import Audio
from .slerp_sprite import SlerpSprite
from .settings import *
#from .leds import Leds
import importlib

class MainLoop:

    def __init__(self):
#        self.leds = Leds()

        # Load routine
        routine_name = "routine_ascend"
        # It's a bit of a hack to get the paths right, but it works for now
        routine_module = importlib.import_module(f"routines.{routine_name}.routine")

        # Used to run one-off events in the future
        self.event_scheduler = EventScheduler()

        # Controls the liquid munging hardware
        self.dispenser = Dispenser()

        # Controls audio
        self.audio = Audio()

        # Initialize Pygame
        pygame_functions.screenSize(SCREEN_WIDTH, SCREEN_HEIGHT, None, None, IS_FULLSCREEN)
        pygame_functions.setBackgroundImage(BG_IMAGE)
        pygame_functions.setAutoUpdate(False)
        self.screen = pygame_functions.screen
        pygame.display.set_caption(WINDOW_CAPTION)

        # Buttons currently onscreen
        self.buttons = []
        self.admin_button = Button(self.screen, pygame.Rect(SCREEN_WIDTH - BUTTON_DEBUG_SIZE, SCREEN_HEIGHT - BUTTON_DEBUG_SIZE, BUTTON_DEBUG_SIZE, BUTTON_DEBUG_SIZE), None, None, self.page_admin)

        # Currently playing sound, if any
        self.last_played_audio = None

        # Initialize Slerp animation
        self.slerp_sprite = SlerpSprite()

        # Time we started to idle. Set to None when not idle.
        self.started_idling = None

        self.drinks = routine_module.get_drinks(self)
        self._get_start_scene = routine_module.get_start_scene
        self._get_drinks_scene = routine_module.get_drinks_scene
        
        self.current_scene = None

    def set_scene(self, scene):
        self.current_scene = scene
        self.current_scene.run()

    def show_drink_buttons(self):
        buttons = []
        y_pos = 0
        for drink_name, drink in self.drinks.items():
            buttons.append(Button(self.screen, pygame.Rect(50, 50 + y_pos * 110, 570, 80), drink.name, drink.rgb, drink.page_function))
            y_pos += 1
        self.set_buttons(buttons)

    def start(self):
        self.set_scene(self._get_start_scene(self))

    def schedule_idling(self, delay):
        self.event_scheduler.schedule(delay, self.start_idling)

    def start_idling(self):
        self.slerp_sprite.start_anim(self.slerp_sprite.animIdling)
        idle_clips = ['slerp_idle1', 'slerp_idle2', 'slerp_idle3']
        clip = self.audio.play(random.choice(idle_clips), -1)
        self.idle_timeout = pygame.time.get_ticks() + (clip.get_length() * 1000)

    def stop_idling(self):
        self.event_scheduler.cancel('start_idling')
        self.idle_timeout = None

    def check_idling_timeout(self):
        if self.idle_timeout and pygame.time.get_ticks() > self.idle_timeout:
            self.set_scene(SceneOne(self))

    def reset_scene(self):
        self.stop_idling()
        self.reset_buttons()

    def page_admin(self):
        pygame_functions.stopMusic()
        self.event_scheduler.cancel_all()
        self.set_buttons([
            Button(self.screen, pygame.Rect(50, 25, 570, 70), 'RESTART', (50, 255, 50), lambda: self.set_scene(self._get_start_scene(self))),
            Button(self.screen, pygame.Rect(50, 110, 570, 70), 'DRINKS SCREEN', (50, 50, 255), lambda: self.set_scene(self._get_drinks_scene(self))),
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
        self.buttons.append(self.admin_button)

    def reset_buttons(self):
        self.buttons = [self.admin_button]
        pygame_functions.setBackgroundImage(BG_IMAGE)

    def play_slerp_audio(self, audio):
        pass

    def handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_loop_running = False
            if event.type == MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.trigger_if_clicked(event.pos)

    def stop_loop(self):
        self.is_loop_running = False
            
    def run(self):
        self.is_loop_running = True
        while self.is_loop_running:
            self.handle_pygame_events()
            self.event_scheduler.execute_due()
            self.dispenser.refresh()
            self.slerp_sprite.refresh()
            self.audio.refresh()
            self.check_idling_timeout()
            for button in self.buttons:
                button.draw()
            pygame_functions.updateDisplay()
            pygame_functions.tick(24)

    def shut_down(self):
        print('Shutting down')
        pygame.quit()
