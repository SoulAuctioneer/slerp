from ..base_scene import Scene
from .scene_six import SceneSix
from src.service_locator import ServiceLocator

class SceneFive(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")

    def run(self):
        audio_service = ServiceLocator.get("audio")
        clip_length = audio_service.audio_files['scene5'].get_length()

        self._event_manager.publish("PLAY_AUDIO", name="scene5")
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)

        self._event_scheduler.schedule(clip_length, self._event_manager.publish, "CHANGE_SCENE", scene_class=SceneSix)
        
        # Schedule bubbles
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=1, pump_name='cyan', duration=4)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=5, pump_name='magenta', duration=5)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=10, pump_name='yellow', duration=5)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=12, pump_name='transparent', duration=5) 