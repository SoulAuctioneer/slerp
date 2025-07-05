import pygame
from ..base_scene import Scene
from src.service_locator import ServiceLocator
from .scene_sleeping import SceneSleeping

class SceneOutro(Scene):

    SPEECH_TEXT = "Ugh... do you have ANY idea how dehydrating that is?! Right, that's quite enough emotional labor for one day. Drink up, and you'll be a normal person again. You're welcome. Now bugger off!"

    def __init__(self, screen, **kwargs):
        super().__init__(screen, **kwargs)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self._speech_complete = False

    def run(self):
        # Start with tired animation
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="tired", loops=0)
        
        # Schedule speech synthesis
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=self.SPEECH_TEXT, callback=self.on_speech_complete)

    def on_speech_complete(self):
        """Called when speech synthesis and playback is complete"""
        self._speech_complete = True
        
        # Wait a moment, then transition back to sleeping scene
        self._event_scheduler.schedule(1, self._event_manager.publish, "CHANGE_SCENE", scene_class=SceneSleeping)
