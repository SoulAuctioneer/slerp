from routines.base_routine import BaseRoutine
from src.drink import Drink
from .scene_one import SceneOne
from .scene_ten import SceneTen
from .scene_nine import SceneNine
from src.service_locator import ServiceLocator

class Routine(BaseRoutine):
    def load(self):
        # In a more complex routine, you would load assets here
        pass

    def get_start_scene(self):
        return SceneOne

    def get_drinks_scene(self):
        return SceneNine

    def get_drinks(self):
        return {
            "invisibility": Drink("INVISIBILITY", (0, 200, 255), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneTen, power='invisibility')),
            "teleportation": Drink("TELEPORTATION", (255, 0, 255), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneTen, power='teleportation')),
            "telekinesis": Drink("TELEKINESIS", (255, 200, 0), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneTen, power='telekinesis')),
            "clairvoyance": Drink("CLAIRVOYANCE", (255, 64, 64), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneTen, power='clairvoyance')),
            "omnilingualism": Drink("OMNILINGUALISM", (0, 255, 64), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneTen, power='omnilingualism')),
            "flight": Drink("FLIGHT", (64, 64, 255), (10, 10, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneTen, power='flight'))
        }

def get_routine(app):
    return Routine(app) 