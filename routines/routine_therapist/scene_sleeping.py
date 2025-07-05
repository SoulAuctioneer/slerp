import random
import pygame
import pygame_functions

from ..base_scene import Scene
from .scene_intro import SceneIntro
from src.button import Button
from src.settings import SNORE_LOUD, PLAY_MUSIC, MUSIC, BUTTON_BG_COLOR

class SceneSleeping(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen, **kwargs)
        self.logo_sprite = None

    def run(self):
        # Show the therablaster logo on the left half of the screen
        self._show_logo_sprite()
        
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="sleeping", loops=0)
        
        buttons = [
            Button(self.screen, pygame.Rect(100, 500, 520, 160), "THERAPIZE ME!", BUTTON_BG_COLOR, self.next_scene)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

        if PLAY_MUSIC:
            self._event_manager.publish("PLAY_MUSIC", name=random.choice(MUSIC))
        
        if SNORE_LOUD:
            self._event_manager.publish("PLAY_AUDIO", name='scene1-loud', loops=-1)
        else:
            self._event_manager.publish("PLAY_AUDIO", name='scene1-quiet', loops=-1)

    def _show_logo_sprite(self):
        """Create and show the therablaster logo sprite on the left half of the screen"""
        self.logo_sprite = pygame_functions.makeSprite("assets/logo-therablaster.png")
        
        # Position on the left half of the screen (adjust as needed)
        logo_x = 140  # Left side positioning
        logo_y = 55  # Vertical center roughly
        
        # Scale the logo if needed (adjust scale factor as appropriate)
        try:
            pygame_functions.transformSprite(self.logo_sprite, 0, 0.5)  # Scale down to 30% of original size
        except:
            # If transformSprite doesn't work, position will be adjusted for larger sprite
            logo_x = 25
            
        pygame_functions.moveSprite(self.logo_sprite, logo_x, logo_y)
        pygame_functions.showSprite(self.logo_sprite)

    def next_scene(self):
        # Hide the logo sprite when transitioning to the next scene
        if self.logo_sprite:
            pygame_functions.hideSprite(self.logo_sprite)
            
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneIntro) 