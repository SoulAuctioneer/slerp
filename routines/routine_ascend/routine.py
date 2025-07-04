from src.drink import Drink
from .scene_one import SceneOne
from .scene_ten import SceneTen
from .scene_nine import SceneNine

def get_drinks(main_loop):
    return {
        "invisibility": Drink("INVISIBILITY", (0, 200, 255), (10, 5, 10, 10), lambda: main_loop.set_scene(SceneTen(main_loop, 'invisibility'))), # cyan
        "teleportation": Drink("TELEPORTATION", (255, 0, 255), (10, 5, 10, 10), lambda: main_loop.set_scene(SceneTen(main_loop, 'teleportation'))), # magenta
        "telekinesis": Drink("TELEKINESIS", (255, 200, 0), (10, 5, 10, 10), lambda: main_loop.set_scene(SceneTen(main_loop, 'telekinesis'))), # yellow
        "clairvoyance": Drink("CLAIRVOYANCE", (255, 64, 64), (10, 5, 10, 10), lambda: main_loop.set_scene(SceneTen(main_loop, 'clairvoyance'))), # red
        "omnilingualism": Drink("OMNILINGUALISM", (0, 255, 64), (10, 5, 10, 10), lambda: main_loop.set_scene(SceneTen(main_loop, 'omnilingualism'))), # green
        "flight": Drink("FLIGHT", (64, 64, 255), (10, 10, 10, 10), lambda: main_loop.set_scene(SceneTen(main_loop, 'flight'))) # blue
    }

def get_start_scene(main_loop):
    return SceneOne(main_loop)

def get_drinks_scene(main_loop):
    return SceneNine(main_loop) 