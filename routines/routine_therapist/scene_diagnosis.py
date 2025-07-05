import pygame
from ..base_scene import Scene
from src.button import Button
from src.settings import BUTTON_BG_COLOR
from src.service_locator import ServiceLocator

class SceneDiagnosis(Scene):
    def __init__(self, screen, diagnosis_key=None, **kwargs):
        super().__init__(screen)
        self.diagnosis_key = diagnosis_key
        self._speech_complete = False
        
    def run(self):
        # Get the routine and fetch diagnosis configuration
        app = ServiceLocator.get("app")
        routine = app.routine
        
        if not self.diagnosis_key:
            # If no diagnosis key provided, get it from routine state
            self.diagnosis_key = routine.get_state("current_diagnosis")
        
        if not self.diagnosis_key:
            # Fallback - shouldn't happen but just in case
            self.diagnosis_key = "default"
        
        # Get the diagnosis config
        diagnosis_config = routine.get_config("diagnoses", {}).get(self.diagnosis_key, {})
        
        # Set animation
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # Get speech text
        speech_text = diagnosis_config.get("speech_text", "I don't know what's wrong with you.")
        
        # Schedule speech synthesis
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=speech_text, callback=self.on_speech_complete)
        
        # Schedule bubbles based on config
        bubbles = diagnosis_config.get("bubbles", [])
        for bubble in bubbles:
            self._event_manager.publish("SCHEDULE_BUBBLE", 
                                      start_timer=bubble.get("start_timer", 1),
                                      pump_name=bubble.get("pump_name", "cyan"),
                                      duration=bubble.get("duration", 3))

    def on_speech_complete(self):
        """Called when speech synthesis and playback is complete"""
        self._speech_complete = True
        
        # Create continue button
        buttons = [
            Button(self.screen, pygame.Rect(100, 300, 520, 120), "CURE ME", BUTTON_BG_COLOR, self.continue_therapy)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)
        self._event_manager.publish("SCHEDULE_IDLING")

    def continue_therapy(self):
        # Transition to the antidote scene with the diagnosis key
        from .scene_antidote import SceneAntidote
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneAntidote, diagnosis_key=self.diagnosis_key) 