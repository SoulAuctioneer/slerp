import pygame
from ..base_scene import Scene
from src.button import Button
from .scene_diagnosis import SceneDiagnosis
from src.service_locator import ServiceLocator
from src.settings import DEBUG_INSTANT_BUTTONS

class SceneIntro(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self._speech_complete = False

    def run(self):
        # The speech text as specified
        speech_text = "AAH!! How's a hyperintelligent supercomputer supposed to get any bloody sleep around here?? ... Well, let's get on with it ... Ahem... Hello! I'm Slerp the Therablaster, here to blast your traumas away. I'll do a deep diagnosis and mix a custom therapeutic cocktail... My first question: What the fuck is wrong with you, anyway?"
        
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
        buttons = [
            Button(self.screen, pygame.Rect(50, 30, 650, 100), 'MOM HATES ME', (255, 100, 100), self.scene_mom_hates_me),
            Button(self.screen, pygame.Rect(50, 140, 650, 100), 'I HATE MYSELF', (100, 100, 255), self.scene_hate_myself),
            Button(self.screen, pygame.Rect(50, 250, 650, 100), 'PENIS ENVY', (255, 255, 100), self.scene_penis_envy),
            Button(self.screen, pygame.Rect(50, 360, 650, 100), 'I HAVE NO SOUL', (100, 255, 100), self.scene_no_soul),
            Button(self.screen, pygame.Rect(50, 470, 650, 100), 'FEAR OF BUTTERFLIES', (0, 200, 255), self.scene_butterfly_phobia),
            Button(self.screen, pygame.Rect(50, 580, 650, 100), 'REALITY TV ADDICT', (255, 0, 255), self.scene_reality_tv_addiction)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

    def scene_mom_hates_me(self):
        self._go_to_diagnosis("mom_hates_me")
        
    def scene_hate_myself(self):
        self._go_to_diagnosis("hate_myself")
        
    def scene_penis_envy(self):
        self._go_to_diagnosis("penis_envy")
        
    def scene_no_soul(self):
        self._go_to_diagnosis("no_soul")
        
    def scene_butterfly_phobia(self):
        self._go_to_diagnosis("butterfly_phobia")
        
    def scene_reality_tv_addiction(self):
        self._go_to_diagnosis("reality_tv_addiction")
    
    def _go_to_diagnosis(self, diagnosis_key):
        """Helper method to transition to diagnosis scene with the given key"""
        # Set the diagnosis key in the routine state
        app = ServiceLocator.get("app")
        app.routine.set_state("current_diagnosis", diagnosis_key)
        
        # Change to the diagnosis scene
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneDiagnosis) 