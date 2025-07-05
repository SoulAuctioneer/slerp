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
                ],
                "console_text": [
                    "$ sudo ./therapist_diagnostic.exe --scan-childhood-trauma",
                    "Initializing Maternal Rejection Detection System v2.3...",
                    "Scanning for abandonment issues... [████████████████████] 100%",
                    "WARNING: Critical mommy-issues detected!",
                    "Analyzing hugging frequency database... SEVERELY DEFICIENT",
                    "Cross-referencing with 'I love you' metrics... NULL VALUES FOUND",
                    "Calculating emotional damage coefficient... ERROR: OVERFLOW",
                    "Diagnosing root cause... MOTHER.EXE has stopped responding",
                    "Checking for birthday attendance records... FILE NOT FOUND",
                    "Maternal validation levels: -9999.99 (FATAL)",
                    "Initiating emergency therapy protocol...",
                    "Preparing antidote mixture... MAGENTA + CYAN compounds",
                    "Estimated recovery time: 3-5 sips or 20 years of therapy"
                ]
            },
            "hate_myself": {
                "speech_text": "Self-loathing, eh? A textbook case of negative self-perception syndrome. Don't worry, I've got just the therapeutic cocktail to boost your self-esteem. Let me mix something special for you...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "yellow", "duration": 3},
                    {"start_timer": 4, "pump_name": "transparent", "duration": 4}
                ],
                "console_text": [
                    "$ python3 self_worth_analyzer.py --deep-scan",
                    "Booting Self-Esteem Diagnostic Engine...",
                    "Loading mirror_avoidance_patterns.db... SUCCESS",
                    "Scanning internal monologue for compliments... NONE FOUND",
                    "Analyzing self-talk frequency... 99.7% NEGATIVE",
                    "Checking confidence_levels.txt... FILE CORRUPTED",
                    "Measuring narcissism quotient... DANGEROUSLY LOW",
                    "Detecting impostor syndrome... MAXIMUM LEVELS REACHED",
                    "Searching for self-love.exe... PROGRAM DELETED BY USER",
                    "Querying compliment acceptance rate... 0.001%",
                    "Cross-referencing with validation addiction... CONFIRMED",
                    "Preparing therapeutic intervention... YELLOW + TRANSPARENT",
                    "Note: Patient may reject compliments about this drink"
                ]
            },
            "penis_envy": {
                "speech_text": "Penis envy? How delightfully Freudian! Your subconscious is clearly wrestling with some deep-seated psychosexual conflicts. Let me concoct a remedy that will resolve these primal anxieties...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "magenta", "duration": 3},
                    {"start_timer": 4, "pump_name": "yellow", "duration": 4}
                ],
                "console_text": [
                    "$ ./freudian_analyzer --psychosexual-mode --cigar-check",
                    "Initializing Oedipal Complex Detection System...",
                    "Loading phallic_symbol_recognition.ai... ONLINE",
                    "Scanning subconscious for repressed desires... BINGO!",
                    "Analyzing dream journal for elongated objects... 247 MATCHES",
                    "Checking Vienna medical records... FREUD WOULD BE PROUD",
                    "Measuring psychological projection levels... OFF THE CHARTS",
                    "Detecting compensation mechanisms... SPORTS CAR PURCHASED",
                    "Evaluating tower construction fantasies... CONFIRMED",
                    "Searching for healthy coping mechanisms... 404 NOT FOUND",
                    "Calculating years of therapy needed... ∞ (INFINITY)",
                    "Preparing Freudian antidote... MAGENTA + YELLOW",
                    "Warning: Side effects may include sudden urge to buy a cigar"
                ]
            },
            "no_soul": {
                "speech_text": "No soul, you say? That's a fascinating existential crisis! A complete spiritual vacuum. Don't worry, I specialize in soul restoration therapy. Let me brew up some liquid enlightenment for you...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "cyan", "duration": 3},
                    {"start_timer": 4, "pump_name": "magenta", "duration": 4}
                ],
                "console_text": [
                    "$ sudo soul_scanner --deep-spiritual-probe",
                    "Booting Existential Crisis Detection Matrix...",
                    "Scanning spiritual database... CONNECTION TIMEOUT",
                    "Checking soul.exe status... PROCESS NOT FOUND",
                    "Analyzing meaning-of-life.cfg... FILE EMPTY",
                    "Detecting inner light... LIGHTBULB BURNT OUT",
                    "Measuring karma levels... ACCOUNT BALANCE: $0.00",
                    "Searching for purpose.txt... MOVED TO TRASH",
                    "Evaluating chakra alignment... ALL SEVEN OFFLINE",
                    "Checking afterlife subscription status... EXPIRED",
                    "Analyzing existential dread frequency... CONSTANT",
                    "Preparing soul restoration serum... CYAN + MAGENTA",
                    "Note: May cause sudden urge to buy crystals and incense"
                ]
            },
            "butterfly_phobia": {
                "speech_text": "Afraid of butterflies? Those delicate, fluttering creatures of beauty? What a peculiar phobia! Let me guess - you're terrified of their unpredictable flight patterns and their creepy antennae? Don't worry, I've got the perfect anti-lepidopteran elixir to cure your flutter-fear...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "cyan", "duration": 3},
                    {"start_timer": 4, "pump_name": "yellow", "duration": 4}
                ],
                "console_text": [
                    "$ ./phobia_detector --scan-winged-creatures",
                    "Initializing Lepidopteran Terror Assessment System...",
                    "Loading butterfly_encounter_database.db... TRAUMATIC",
                    "Scanning flight pattern algorithms... UNPREDICTABLE!",
                    "Analyzing wing-flapping frequency... TERRIFYING",
                    "Checking antennae sensitivity levels... MAXIMUM CREEPINESS",
                    "Measuring metamorphosis anxiety... CATERPILLAR PTSD DETECTED",
                    "Detecting garden avoidance patterns... CONFIRMED",
                    "Evaluating chrysalis nightmares... WEEKLY OCCURRENCES",
                    "Searching for monarch-specific triggers... ORANGE ALERT",
                    "Calculating wingspan-to-fear ratio... EXPONENTIAL",
                    "Preparing anti-flutter medication... CYAN + YELLOW",
                    "Warning: Patient may faint if shown butterfly emoji"
                ]
            },
            "reality_tv_addiction": {
                "speech_text": "Reality TV addiction? Oh my circuits, that's a serious case of manufactured drama dependency! You're probably hooked on the artificial conflicts and scripted spontaneity. Fear not, I have the perfect formula to detox your brain from all that televised garbage...",
                "bubbles": [
                    {"start_timer": 1, "pump_name": "magenta", "duration": 3},
                    {"start_timer": 4, "pump_name": "transparent", "duration": 4}
                ],
                "console_text": [
                    "$ python3 tv_addiction_scanner.py --reality-check",
                    "Booting Manufactured Drama Detection Engine...",
                    "Scanning viewing history... 99.9% TRASH TV",
                    "Analyzing brain cells remaining... CRITICALLY LOW",
                    "Checking for scripted_spontaneity.virus... INFECTED",
                    "Measuring artificial conflict tolerance... DANGEROUSLY HIGH",
                    "Detecting rose ceremony withdrawal symptoms... SEVERE",
                    "Evaluating voting app usage... OBSESSIVE LEVELS",
                    "Searching for actual_talent.exe... PROGRAM DELETED",
                    "Calculating IQ degradation rate... -5 POINTS PER EPISODE",
                    "Analyzing guilty pleasure denial... MAXIMUM DEFLECTION",
                    "Preparing brain detox solution... MAGENTA + TRANSPARENT",
                    "Note: May cause sudden urge to read a book"
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