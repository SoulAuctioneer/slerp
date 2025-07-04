import random
import pygame

from ..base_scene import Scene
from .scene_two import SceneTwo
from src.button import Button
from src.service_locator import ServiceLocator
from src.settings import SNORE_LOUD, PLAY_MUSIC, MUSIC, BUTTON_BG_COLOR

class SceneOne(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self.button = Button(self.screen, pygame.Rect(100, 300, 520, 240), "WAKE UP, SLERP!", BUTTON_BG_COLOR, self.next_scene)

    def run(self):
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="sleeping", loops=0)
        
        if PLAY_MUSIC:
            self._event_manager.publish("PLAY_MUSIC", name=random.choice(MUSIC))
        
        if SNORE_LOUD:
            self._event_manager.publish("PLAY_AUDIO", name='scene1-loud', loops=-1)
        else:
            self._event_manager.publish("PLAY_AUDIO", name='scene1-quiet', loops=-1)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button.trigger_if_clicked(event.pos)

    def draw(self, screen):
        self.button.draw(screen)

    def next_scene(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneTwo) 