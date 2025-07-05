import pygame
from ..base_scene import Scene
from src.button import Button
from src.service_locator import ServiceLocator
from src.settings import DEBUG_INSTANT_BUTTONS

class SceneIntro(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self._speech_complete = False

    def run(self):
        # The new revised speech text
        speech_text = "AAH!! How's a hyperintelligent supercomputer supposed to get any bloody sleep around here?? ... Well, let's get on with it ... Ahem... Hello! I'm Slerp the Therablaster, here to blast your traumas away with a custom therapeutic slushie! Let's get started; I bill by the second."
        
        # Start speech synthesis
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=speech_text, callback=self.on_speech_complete)
        
        # Animation sequence
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="tired", loops=0)
        self._event_scheduler.schedule(5.9, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="waking", loops=0) 
        self._event_scheduler.schedule(7.5, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="angry", loops=0)
        self._event_scheduler.schedule(8.7, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # Schedule bubbles
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=1, pump_name='cyan', duration=4)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=5, pump_name='magenta', duration=5)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=10, pump_name='yellow', duration=5)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=12, pump_name='transparent', duration=5)

        # Show buttons instantly if debug flag is enabled
        if DEBUG_INSTANT_BUTTONS:
            self.create_buttons()

    def on_speech_complete(self):
        """Called when speech synthesis and playback is complete"""
        self._speech_complete = True
        self.create_buttons()
        self._event_manager.publish("SCHEDULE_IDLING")

    def create_buttons(self):
        # Start the existential calibration with question 1
        from .scene_question1 import SceneQuestion1
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneQuestion1) 