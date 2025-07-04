import pygame
from ..base_scene import Scene
from src.service_locator import ServiceLocator
from src.button import Button

class SceneNine(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self.buttons = []

    def run(self):
        audio_service = ServiceLocator.get("audio")
        clip_length = audio_service.audio_files['scene9'].get_length()

        self._event_manager.publish("PLAY_AUDIO", name="scene9")
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        self._event_scheduler.schedule(clip_length, self._event_manager.publish, "SCHEDULE_IDLING")
        
        app = ServiceLocator.get("app")
        drinks = app.routine.get_drinks()
        y_pos = 0
        for drink in drinks.values():
            button = Button(self.screen, pygame.Rect(50, 50 + y_pos * 110, 570, 80), drink.name, drink.rgb, drink.page_function)
            self.buttons.append(button)
            y_pos += 1

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.trigger_if_clicked(event.pos)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen) 