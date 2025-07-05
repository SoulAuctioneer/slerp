from routines.base_routine import BaseRoutine
from src.drink import Drink
from .scene_sleeping import SceneSleeping
from .scene_intro import SceneIntro
from .scene_antidote import SceneAntidote
from .scene_outro import SceneOutro
from src.service_locator import ServiceLocator

class Routine(BaseRoutine):
    def load(self):
        # Set up diagnosis configurations
        diagnoses_config = {
            "mom_hates_me": {
                "speech_text": "Ah yes, the classic maternal rejection complex. Let me analyze your mommy issues while I prepare the perfect antidote. This is going to require some serious therapeutic intervention...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "magenta", "duration": 3},
                    {"start_timer": 4, "pump_name": "cyan", "duration": 4}
                ]
            },
            "hate_myself": {
                "speech_text": "Self-loathing, eh? A textbook case of negative self-perception syndrome. Don't worry, I've got just the therapeutic cocktail to boost your self-esteem. Let me mix something special for you...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "yellow", "duration": 3},
                    {"start_timer": 4, "pump_name": "transparent", "duration": 4}
                ]
            },
            "penis_envy": {
                "speech_text": "Penis envy? How delightfully Freudian! Your subconscious is clearly wrestling with some deep-seated psychosexual conflicts. Let me concoct a remedy that will resolve these primal anxieties...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "magenta", "duration": 3},
                    {"start_timer": 4, "pump_name": "yellow", "duration": 4}
                ]
            },
            "no_soul": {
                "speech_text": "No soul, you say? That's a fascinating existential crisis! A complete spiritual vacuum. Don't worry, I specialize in soul restoration therapy. Let me brew up some liquid enlightenment for you...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "cyan", "duration": 3},
                    {"start_timer": 4, "pump_name": "magenta", "duration": 4}
                ]
            },
            "butterfly_phobia": {
                "speech_text": "Afraid of butterflies? Those delicate, fluttering creatures of beauty? What a peculiar phobia! Let me guess - you're terrified of their unpredictable flight patterns and their creepy antennae? Don't worry, I've got the perfect anti-lepidopteran elixir to cure your flutter-fear...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "cyan", "duration": 3},
                    {"start_timer": 4, "pump_name": "yellow", "duration": 4}
                ]
            },
            "reality_tv_addiction": {
                "speech_text": "Reality TV addiction? Oh my circuits, that's a serious case of manufactured drama dependency! You're probably hooked on the artificial conflicts and scripted spontaneity. Fear not, I have the perfect formula to detox your brain from all that televised garbage...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "magenta", "duration": 3},
                    {"start_timer": 4, "pump_name": "transparent", "duration": 4}
                ]
            }
        }
        
        # Set the config
        self.set_config({
            "diagnoses": diagnoses_config
        })

    def get_start_scene(self):
        return SceneSleeping

    def get_drinks_scene(self):
        # For now, just return SceneIntro - could be expanded later
        return SceneIntro

    def get_drinks(self):
        # Simple therapy drinks for now
        return {
            "confidence": Drink("CONFIDENCE", (255, 215, 0), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneIntro)),
            "happiness": Drink("HAPPINESS", (255, 192, 203), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneIntro)),
            "clarity": Drink("CLARITY", (135, 206, 235), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneIntro)),
            "zen": Drink("ZEN", (144, 238, 144), (10, 5, 10, 10), lambda: ServiceLocator.get("event_manager").publish("CHANGE_SCENE", scene_class=SceneIntro))
        }

def get_routine(app):
    return Routine(app) 