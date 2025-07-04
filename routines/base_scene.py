import pygame
from src.service_locator import ServiceLocator

class Scene:
    def __init__(self, screen, **kwargs):
        self.screen = screen
        self._event_manager = ServiceLocator.get("event_manager")

    def run(self):
        """Called when the scene is first loaded."""
        pass

    def update(self):
        """Called every frame."""
        pass

    def draw(self, screen):
        """Called every frame to draw to the screen."""
        pass
    
    def handle_events(self, events):
        """Handle pygame events."""
        pass 