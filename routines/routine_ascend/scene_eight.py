import pygame
from ..base_scene import Scene
from src.button import Button
from .scene_nine import SceneNine
from src.service_locator import ServiceLocator
from src.settings import BUTTON_BG_COLOR

class SceneEight(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")

    def run(self):
        audio_service = ServiceLocator.get("audio")
        clip_length = audio_service.audio_files['scene8'].get_length()

        self._event_manager.publish("PLAY_AUDIO", name="scene8")
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        self._event_scheduler.schedule(clip_length, self._event_manager.publish, "SCHEDULE_IDLING")

        button_timing = clip_length - 2
        self._event_scheduler.schedule(button_timing, self.create_buttons)

    def create_buttons(self):
        buttons = [
            Button(self.screen, pygame.Rect(100, 300, 520, 240), "OK", (255, 0, 255), self.next_scene)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

    def next_scene(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneNine) 