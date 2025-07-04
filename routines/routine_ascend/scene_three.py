from ..base_scene import Scene
from .scene_eight import SceneEight
from src.service_locator import ServiceLocator

class SceneThree(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")

    def run(self):
        audio_service = ServiceLocator.get("audio")
        clip_length = audio_service.audio_files['scene3'].get_length()
        
        self._event_manager.publish("PLAY_AUDIO", name="scene3")
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="angry", loops=0)
        
        self._event_scheduler.schedule(clip_length, self._event_manager.publish, "CHANGE_SCENE", scene_class=SceneEight) 