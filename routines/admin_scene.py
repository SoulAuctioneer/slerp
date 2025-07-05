import pygame
from .base_scene import Scene
from src.button import Button
from src.service_locator import ServiceLocator

class AdminScene(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self._event_scheduler.cancel_all()
        
    def run(self):
        start_scene_class = ServiceLocator.get("app").routine.get_start_scene()
        drinks_scene_class = ServiceLocator.get("app").routine.get_drinks_scene()

        buttons = [
            Button(self.screen, pygame.Rect(50, 25, 570, 70), 'RESTART', (50, 255, 50), lambda: self._event_manager.publish("CHANGE_SCENE", scene_class=start_scene_class)),
            Button(self.screen, pygame.Rect(50, 110, 570, 70), 'DRINKS SCREEN', (50, 50, 255), lambda: self._event_manager.publish("CHANGE_SCENE", scene_class=drinks_scene_class)),
            Button(self.screen, pygame.Rect(50, 195, 570, 70), 'TEST CYAN', (0, 255, 255), lambda: self._event_manager.publish("TEST_PUMP", pump_name='cyan')),
            Button(self.screen, pygame.Rect(50, 280, 570, 70), 'TEST MAGENTA', (255, 0, 255), lambda: self._event_manager.publish("TEST_PUMP", pump_name='magenta')),
            Button(self.screen, pygame.Rect(50, 365, 570, 70), 'TEST YELLOW', (255, 255, 0), lambda: self._event_manager.publish("TEST_PUMP", pump_name='yellow')),
            Button(self.screen, pygame.Rect(50, 450, 570, 70), 'TEST TRANSPARENT', (150, 150, 165), lambda: self._event_manager.publish("TEST_PUMP", pump_name='transparent')),
            Button(self.screen, pygame.Rect(50, 535, 570, 70), 'TEST PRIMING', (180, 128, 128), lambda: self._event_manager.publish("TEST_PRIME")),
            Button(self.screen, pygame.Rect(50, 620, 570, 70), 'EXIT', (255, 50, 50), self.exit_app)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

    def exit_app(self):
        ServiceLocator.get("app").is_running = False 