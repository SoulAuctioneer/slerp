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
        self.buttons = []

    def run(self):
        audio_service = ServiceLocator.get("audio")
        clip_length = audio_service.audio_files['scene8'].get_length()

        self._event_manager.publish("PLAY_AUDIO", name="scene8")
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        self._event_scheduler.schedule(clip_length, self._event_manager.publish, "SCHEDULE_IDLING")
        
        self._event_scheduler.schedule(22, self.create_buttons)

    def create_buttons(self):
        self.buttons = [
            Button(self.screen, pygame.Rect(100, 300, 520, 240), "OK", BUTTON_BG_COLOR, self.next_scene)
        ]

    def next_scene(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneNine)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.trigger_if_clicked(event.pos)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen) 