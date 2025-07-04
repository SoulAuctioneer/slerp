import pygame
from ..base_scene import Scene
from src.button import Button
from .scene_three import SceneThree
from .scene_four import SceneFour
from src.service_locator import ServiceLocator
from src.settings import BUTTON_BG_COLOR

class SceneTwo(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")

    def run(self):
        self._event_manager.publish("STOP_MUSIC")
        self._event_manager.publish("PLAY_AUDIO", name='scene2')
        
        audio_service = ServiceLocator.get("audio")
        clip_length = audio_service.audio_files['scene2'].get_length()

        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="tired", loops=0)
        self._event_scheduler.schedule(6.0, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="waking", loops=0) 
        self._event_scheduler.schedule(7.5, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="angry", loops=0)
        self._event_scheduler.schedule(8.7, self._event_manager.publish, "SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # Schedule button appearance
        self._event_scheduler.schedule(clip_length - 3, self.create_buttons)
        # Schedule idling
        self._event_scheduler.schedule(clip_length, self._event_manager.publish, "SCHEDULE_IDLING")

        # Schedule bubbles
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=1, pump_name='cyan', duration=4)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=5, pump_name='magenta', duration=5)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=10, pump_name='yellow', duration=5)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=12, pump_name='transparent', duration=5)

    def create_buttons(self):
        buttons = [
            Button(self.screen, pygame.Rect(50, 420-60, 570, 150), 'YES', (50, 255, 50), self.scene_three),
            Button(self.screen, pygame.Rect(50, 225-60, 570, 150), 'NO', (255, 50, 50), self.scene_four)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

    def scene_three(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneThree)
        
    def scene_four(self):
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneFour) 