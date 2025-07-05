import pygame
from ..base_scene import Scene
from src.button import Button
from .scene_mom_hates_me import SceneMomHatesMe
from .scene_hate_myself import SceneHateMyself
from .scene_penis_envy import ScenePenisEnvy
from .scene_no_soul import SceneNoSoul
from src.service_locator import ServiceLocator

class SceneIntro(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self._speech_complete = False

    def run(self):
        # The speech text as specified
        speech_text = "GAH! How's a hyperintelligent supercomputer supposed to get any bloody sleep around here?? Well, let's get on with it. Hello, esteemed customer! I'm Slerp the Therablaster, here to blast your mental worries away. As a licensed therapist, I'll do a deep diagnosis and mix a custom antidote that will instantly cure you. My first question: What the fuck is wrong with you, anyway?"
        
        # Start speech synthesis
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=speech_text, callback=self.on_speech_complete)
        
        # Animation sequence
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="tired", loops=0)
        self._event_scheduler.schedule(3.0, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="waking", loops=0) 
        self._event_scheduler.schedule(4.5, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="angry", loops=0)
        self._event_scheduler.schedule(6.0, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # Schedule bubbles
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=1, pump_name='cyan', duration=4)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=5, pump_name='magenta', duration=5)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=10, pump_name='yellow', duration=5)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=12, pump_name='transparent', duration=5)

    def on_speech_complete(self):
        """Called when speech synthesis and playback is complete"""
        self._speech_complete = True
        self.create_buttons()
        self._event_manager.publish("SCHEDULE_IDLING")

    def create_buttons(self):
        buttons = [
            Button(self.screen, pygame.Rect(50, 50, 570, 80), 'MOM HATES ME', (255, 100, 100), self.scene_mom_hates_me),
            Button(self.screen, pygame.Rect(50, 160, 570, 80), 'I HATE MYSELF', (100, 100, 255), self.scene_hate_myself),
            Button(self.screen, pygame.Rect(50, 270, 570, 80), 'PENIS ENVY', (255, 255, 100), self.scene_penis_envy),
            Button(self.screen, pygame.Rect(50, 380, 570, 80), 'I HAVE NO SOUL', (100, 255, 100), self.scene_no_soul)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

    def scene_mom_hates_me(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneMomHatesMe)
        
    def scene_hate_myself(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneHateMyself)
        
    def scene_penis_envy(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=ScenePenisEnvy)
        
    def scene_no_soul(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneNoSoul) 