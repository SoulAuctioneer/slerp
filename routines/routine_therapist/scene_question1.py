import pygame
from ..base_scene import Scene
from src.button import Button
from src.service_locator import ServiceLocator
from src.settings import DEBUG_INSTANT_BUTTONS

class SceneQuestion1(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self._speech_complete = False

    def run(self):
        # Question 1 speech text
        speech_text = "First question: If your subconscious was a conspiracy theory, which one would it be?"
        
        # Set animation
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # Start speech synthesis
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=speech_text, callback=self.on_speech_complete)
        
        # Schedule bubbles
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=1, pump_name='cyan', duration=3)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=4, pump_name='magenta', duration=4)

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
            Button(self.screen, pygame.Rect(50, 50, 650, 80), 'FLAT EARTH THEORY', (255, 100, 100), lambda: self.answer_selected("flat_earth", "Ah, denial runs deep.")),
            Button(self.screen, pygame.Rect(50, 150, 650, 80), 'BIRDS AREN\'T REAL', (100, 100, 255), lambda: self.answer_selected("birds_arent_real", "Classic avoidance of reality.")),
            Button(self.screen, pygame.Rect(50, 250, 650, 80), 'MOON LANDING HOAX', (255, 255, 100), lambda: self.answer_selected("moon_landing_hoax", "Trust issues, fascinating.")),
            Button(self.screen, pygame.Rect(50, 350, 650, 80), 'LIZARD PEOPLE RULE', (100, 255, 100), lambda: self.answer_selected("lizard_people", "Paranoia suits you.")),
            Button(self.screen, pygame.Rect(50, 450, 650, 80), 'SIMULATION HYPOTHESIS', (0, 200, 255), lambda: self.answer_selected("simulation_hypothesis", "Comfortably dissociated, I see."))
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

    def answer_selected(self, answer_key, response_text):
        """Handle answer selection with spoken response"""
        # Clear buttons immediately
        self._event_manager.publish("SET_BUTTONS", buttons=[])
        
        # Store the answer
        app = ServiceLocator.get("app")
        app.routine.set_state("question1_answer", answer_key)
        
        # Speak the response
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=response_text, callback=self.proceed_to_question2)
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)

    def proceed_to_question2(self):
        """Move to question 2 after response is spoken"""
        from .scene_question2 import SceneQuestion2
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneQuestion2) 