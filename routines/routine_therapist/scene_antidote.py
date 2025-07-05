import random
import pygame_functions
import math
from ..base_scene import Scene
from src.service_locator import ServiceLocator
from .scene_outro import SceneOutro
from src.settings import MUSIC

class SceneAntidote(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen, **kwargs)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self.brain_juice_sprite = None
        self.brain_juice_animation_active = False
        self.brain_juice_base_y = 30  # Base Y position for bobbing
        self.brain_juice_x = 30  # X position on left side of screen
        self.animation_timer = 0
        self.sprite_scale = 0.6  # Scale down the 1024x1024 image

    def run(self):        
        dispenser = ServiceLocator.get("dispenser")
        app = ServiceLocator.get("app")
        
        # Get the selected diagnosis and determine appropriate drink
        selected_diagnosis = app.routine.get_state("selected_diagnosis")
        drink = self._get_antidote_drink(selected_diagnosis)
        
        # Start talking animation
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # Say opening line
        self._event_manager.publish("SYNTHESIZE_SPEECH", text="Alright, squeezing one out!", show_subtitles=False)
        
        # Start dispensing the drink after 2 seconds
        self._event_scheduler.schedule(2, dispenser.dispense, drink=drink)
        
        # Switch to singing animation when dispensing starts and play music
        self._event_scheduler.schedule(2, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="singing", loops=0)
        self._event_scheduler.schedule(2, self._event_manager.publish, "PLAY_MUSIC", name=random.choice(MUSIC), volume=0.5)
        
        # Show brain-juice sprite when drink starts pouring
        self._event_scheduler.schedule(2, self._show_brain_juice_sprite)
        
        # Say cold line while drink is pouring
        self._event_scheduler.schedule(5, self._event_manager.publish, "SYNTHESIZE_SPEECH", text="Oooh that feels so cold. I'll never get used to that!", show_subtitles=False)
        self._event_scheduler.schedule(5, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="straining", loops=0)
        self._event_scheduler.schedule(8, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="singing", loops=0)
        
        # Say next line a few seconds later
        self._event_scheduler.schedule(10, self._event_manager.publish, "SYNTHESIZE_SPEECH", text="ugh, aggghh...aaahhhhahahahaaaaaa!!!", show_subtitles=False)
        self._event_scheduler.schedule(10, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="straining", loops=0)
        self._event_scheduler.schedule(12.5, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="singing", loops=0)
        
        # Hide brain-juice sprite when drink is done
        self._event_scheduler.schedule(17, self._hide_brain_juice_sprite)

        # A lil more straining
        self._event_scheduler.schedule(16, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="straining", loops=0)
        
        # End scene and go to outro
        self._event_scheduler.schedule(18, self._event_manager.publish, "CHANGE_SCENE", scene_class=SceneOutro)

    def _show_brain_juice_sprite(self):
        """Create and show the brain-juice sprite with animations"""
        self.brain_juice_sprite = pygame_functions.makeSprite("assets/brain-juice.png")
        
        # Try to scale the sprite down to a reasonable size
        try:
            pygame_functions.transformSprite(self.brain_juice_sprite, 0, self.sprite_scale)
        except:
            # If transformSprite doesn't work, we'll work with the original size
            # but adjust position to account for the large sprite
            self.brain_juice_x = 50  # Move further left to account for large sprite
            
        pygame_functions.moveSprite(self.brain_juice_sprite, self.brain_juice_x, self.brain_juice_base_y)
        pygame_functions.showSprite(self.brain_juice_sprite)
        self.brain_juice_animation_active = True
        self.animation_timer = 0

    def _hide_brain_juice_sprite(self):
        """Hide the brain-juice sprite"""
        if self.brain_juice_sprite:
            pygame_functions.hideSprite(self.brain_juice_sprite)
            self.brain_juice_animation_active = False

    def update(self):
        """Update the brain-juice sprite animation"""
        if self.brain_juice_animation_active and self.brain_juice_sprite:
            self.animation_timer += 0.1
            
            # Bobbing motion (up and down) - reduced amplitude
            bob_offset = math.sin(self.animation_timer * 3) * 10  # Reduced from 20 to 10 pixels amplitude
            new_y = self.brain_juice_base_y + bob_offset
            
            # Scaling effect (shrink and expand) - reduced range
            scale_factor = self.sprite_scale * (1.0 + (math.sin(self.animation_timer * 2) * 0.1))  # Reduced from 0.2 to 0.1
            
            # Apply position update
            pygame_functions.moveSprite(self.brain_juice_sprite, self.brain_juice_x, new_y)
            
            # Apply scaling
            try:
                pygame_functions.transformSprite(self.brain_juice_sprite, 0, scale_factor)
            except:
                # If transformSprite doesn't exist, skip scaling
                pass

    def _get_antidote_drink(self, selected_diagnosis):
        """Get the appropriate drink based on the diagnosis"""
        app = ServiceLocator.get("app")
        drinks = app.routine.get_drinks()
        
        # Get the first drink from the diagnosis (or default to confidence)
        drink_names = selected_diagnosis.get("drinks", ["confidence"])
        drink_name = drink_names[0] if drink_names else "confidence"
        
        return drinks.get(drink_name, drinks["confidence"]) 