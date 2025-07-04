import pygame
import pygame_functions
from ..base_scene import Scene
from src.service_locator import ServiceLocator
from .scene_eleven import SceneEleven
from src.settings import BG_IMAGE, BG_IMAGE_SYMBOL

class SceneTen(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen, **kwargs)
        self.power = kwargs.get('power')
        self._event_scheduler = ServiceLocator.get("event_scheduler")

    def run(self):
        pygame_functions.setBackgroundImage(BG_IMAGE_SYMBOL)
        
        audio = ServiceLocator.get("audio")
        dispenser = ServiceLocator.get("dispenser")
        app = ServiceLocator.get("app")
        drink = app.routine.get_drinks()[self.power]
        
        timer = 0
        
        # Audio sequence
        clip = audio.play('scene10-1')
        timer += clip.get_length()
        clip = audio.enqueue('scene10-2-%s' % self.power)
        timer_start_straining = timer
        timer += clip.get_length()
        clip = audio.enqueue('scene10-3')
        timer += clip.get_length()
        timer_start_superpower_disclaimer = timer
        clip = audio.enqueue('scene10-4-%s' % self.power)
        timer += clip.get_length()
        timer_end_scene = timer

        # Animation and hardware sequence
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        self._event_scheduler.schedule(timer_start_straining, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="straining", loops=0)
        self._event_scheduler.schedule(4, dispenser.dispense, drink=drink)
        self._event_scheduler.schedule(timer_start_straining + 11, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="tired", loops=0)
        self._event_scheduler.schedule(timer_start_straining + 30, pygame_functions.setBackgroundImage, BG_IMAGE)
        self._event_scheduler.schedule(timer_start_superpower_disclaimer, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # End scene
        self._event_scheduler.schedule(timer_end_scene, self._event_manager.publish, "CHANGE_SCENE", scene_class=SceneEleven) 