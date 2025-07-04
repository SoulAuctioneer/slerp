import pygame
from ..base_scene import Scene
from src.button import Button
from .scene_seven import SceneSeven
from .scene_eight import SceneEight
from src.service_locator import ServiceLocator
from src.settings import BUTTON_BG_COLOR

class SceneSix(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")

    def run(self):
        audio_service = ServiceLocator.get("audio")
        clip_length = audio_service.audio_files['scene6'].get_length()

        self._event_manager.publish("PLAY_AUDIO", name="scene6")
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        self._event_scheduler.schedule(clip_length, self._event_manager.publish, "SCHEDULE_IDLING")
        
        buttons = [
             Button(self.screen, pygame.Rect(50, 225-60, 570, 150), 'I CONSENT', BUTTON_BG_COLOR, self.scene_eight),
             Button(self.screen, pygame.Rect(50, 420-60, 570, 150), 'I DO NOT CONSENT', BUTTON_BG_COLOR, self.scene_seven)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

    def scene_seven(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneSeven)
        
    def scene_eight(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneEight) 