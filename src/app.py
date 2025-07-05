import pygame
import pygame_functions
from .settings import *
from .service_locator import ServiceLocator
from .event_manager import EventManager
from .scene_manager import SceneManager
from .audio import Audio
from .event_scheduler import EventScheduler
from .slerp_sprite import SlerpSprite
from .dispenser import Dispenser
from .tts_service import TTSService
from .button import Button
from routines.admin_scene import AdminScene
import random
# Import other services as they are refactored
import importlib

class App:
    def __init__(self):
        # Initialize Pygame
        pygame_functions.screenSize(SCREEN_WIDTH, SCREEN_HEIGHT, None, None, IS_FULLSCREEN)
        pygame_functions.setBackgroundImage(BG_IMAGE)
        pygame_functions.setAutoUpdate(False)
        self.screen = pygame_functions.screen
        pygame.display.set_caption(WINDOW_CAPTION)

        # Global UI
        self.admin_button = Button(self.screen, pygame.Rect(SCREEN_WIDTH - BUTTON_DEBUG_SIZE, SCREEN_HEIGHT - BUTTON_DEBUG_SIZE, BUTTON_DEBUG_SIZE, BUTTON_DEBUG_SIZE), None, None, self.show_admin_panel)
        self.buttons = [self.admin_button]

        # Core components
        self.is_running = False
        self.idle_timeout = None
        self.event_manager = EventManager()
        self.event_manager.subscribe("SCHEDULE_IDLING", self.schedule_idling)
        self.event_manager.subscribe("SET_BUTTONS", self.set_buttons)
        
        # Register core components
        ServiceLocator.register("app", self)
        ServiceLocator.register("event_manager", self.event_manager)

        # Services and Managers
        self.event_scheduler = EventScheduler()
        ServiceLocator.register("event_scheduler", self.event_scheduler)
        self.scene_manager = SceneManager()
        self.audio_service = Audio() # Will be refactored to be a proper service
        self.slerp_sprite_service = SlerpSprite()
        self.dispenser_service = Dispenser()
        self.tts_service = TTSService()
        ServiceLocator.register("audio", self.audio_service)
        ServiceLocator.register("slerp_sprite", self.slerp_sprite_service)
        ServiceLocator.register("dispenser", self.dispenser_service)
        ServiceLocator.register("tts", self.tts_service)
        # Register other services...

        # Load routine
        self.load_routine(ACTIVE_ROUTINE)

    def load_routine(self, routine_name):
        routine_module = importlib.import_module(f"routines.{routine_name}.routine")
        self.routine = routine_module.get_routine(self)
        self.routine.load()
        self.event_manager.publish("CHANGE_SCENE", scene_class=self.routine.get_start_scene())

    def set_buttons(self, buttons):
        print(f"DEBUG: set_buttons called with {len(buttons)} buttons")
        for i, button in enumerate(buttons):
            print(f"DEBUG: Button {i}: {button.text if hasattr(button, 'text') else 'No text'}")
        self.reset_buttons()  # Always reset first
        self.buttons = [self.admin_button] + buttons
        print(f"DEBUG: Total buttons after set_buttons: {len(self.buttons)}")

    def reset_buttons(self):
        print(f"DEBUG: reset_buttons called. Before: {len(self.buttons)} buttons")
        self.buttons = [self.admin_button]
        pygame_functions.setBackgroundImage(BG_IMAGE)  # Clear any drawn buttons by resetting background
        print(f"DEBUG: reset_buttons complete. After: {len(self.buttons)} buttons")

    def schedule_idling(self):
        self.event_scheduler.cancel_all() # Cancel any pending scene changes
        self.start_idling()

    def start_idling(self):
        self.event_manager.publish("SET_SLERP_ANIMATION", animation_name="idling", loops=0)
        idle_clips = ['slerp_idle1', 'slerp_idle2', 'slerp_idle3']
        chosen_clip = random.choice(idle_clips)
        clip_length = self.audio_service.audio_files[chosen_clip].get_length()
        self.audio_service.play(chosen_clip, loops=-1)
        self.idle_timeout = pygame.time.get_ticks() + (clip_length * 1000)

    def check_idling_timeout(self):
        if self.idle_timeout and pygame.time.get_ticks() > self.idle_timeout:
            self.idle_timeout = None
            start_scene_class = self.routine.get_start_scene()
            self.event_manager.publish("CHANGE_SCENE", scene_class=start_scene_class)

    def show_admin_panel(self):
        self.event_manager.publish("CHANGE_SCENE", scene_class=AdminScene)

    def run(self):
        self.is_running = True
        frame_count = 0
        while self.is_running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.trigger_if_clicked(event.pos)

            self.scene_manager.handle_events(events)
            self.scene_manager.update()
            
            # Refresh services
            self.event_scheduler.execute_due()
            self.audio_service.refresh()
            self.slerp_sprite_service.refresh()
            self.check_idling_timeout()

            # Drawing
            self.scene_manager.draw(self.screen)
            for button in self.buttons:
                button.draw(self.screen)
            
            # Debug logging every 120 frames (5 seconds at 24fps)
            frame_count += 1
            if frame_count % 120 == 0:
                print(f"DEBUG: Frame {frame_count}, drawing {len(self.buttons)} buttons")
                
            pygame_functions.updateDisplay()
            pygame_functions.tick(24)

    def shut_down(self):
        print("Shutting down...")
        pygame.quit() 