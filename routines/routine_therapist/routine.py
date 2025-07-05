from routines.base_routine import BaseRoutine
from src.drink import Drink
from .scene_sleeping import SceneSleeping
from .scene_intro import SceneIntro
from .scene_antidote import SceneAntidote
from .scene_outro import SceneOutro
from src.service_locator import ServiceLocator

class Routine(BaseRoutine):
    def load(self):
        # No specific configurations needed for the revised flow
        # The random selection happens in the diagnosis scene
        pass

    def get_start_scene(self):
        return SceneSleeping

    def get_drinks_scene(self):
        # For now, just return SceneIntro - could be expanded later
        return SceneIntro

    def get_drinks(self):
        # Updated therapy drinks for the revised routine
        return {
            "confidence": Drink("CONFIDENCE", (255, 215, 0), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneIntro)),
            "happiness": Drink("HAPPINESS", (255, 192, 203), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneIntro)),
            "clarity": Drink("CLARITY", (135, 206, 235), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneIntro)),
            "zen": Drink("ZEN", (144, 238, 144), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneIntro))
        }

def get_routine(app):
    return Routine(app) 