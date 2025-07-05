import pygame
from ..base_scene import Scene
from src.button import Button
from src.settings import BUTTON_BG_COLOR

class SceneMomHatesMe(Scene):
    def run(self):
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # Schedule speech synthesis for this scene
        speech_text = "Ah yes, the classic maternal rejection complex. Let me analyze your mommy issues while I prepare the perfect antidote. This is going to require some serious therapeutic intervention..."
        
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=speech_text, callback=self.on_speech_complete)
        
        # Schedule some bubbles for visual effect
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=1, pump_name='magenta', duration=3)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=4, pump_name='cyan', duration=4)

    def on_speech_complete(self):
        """Called when speech synthesis and playback is complete"""
        buttons = [
            Button(self.screen, pygame.Rect(100, 300, 520, 120), "CONTINUE THERAPY", BUTTON_BG_COLOR, self.continue_therapy)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)
        self._event_manager.publish("SCHEDULE_IDLING")

    def continue_therapy(self):
        # For now, just cycle back to scene intro - could be expanded later
        from .scene_intro import SceneIntro
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneIntro) 