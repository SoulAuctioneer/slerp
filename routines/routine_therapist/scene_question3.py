import pygame
from ..base_scene import Scene
from src.button import Button
from src.service_locator import ServiceLocator
from src.settings import DEBUG_INSTANT_BUTTONS

class SceneQuestion3(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self._speech_complete = False

    def run(self):
        # Question 3 speech text
        speech_text = "Finally, what coping mechanism will you use when AI inevitably replaces you?"
        
        # Start speech synthesis
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=speech_text, callback=self.on_speech_complete)
        
        # Set animation
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # Schedule bubbles
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=1, pump_name='magenta', duration=3)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=4, pump_name='cyan', duration=4)

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
            Button(self.screen, pygame.Rect(20, 30, 710, 80), 'MINDFUL SURRENDER', (255, 100, 100), lambda: self.answer_selected("mindful_surrender", "Zen or just lazy?")),
            Button(self.screen, pygame.Rect(20, 130, 710, 80), 'IRRATIONAL OPTIMISM', (100, 100, 255), lambda: self.answer_selected("overcompensating_optimism", "Delusion masked as hope, charming.")),
            Button(self.screen, pygame.Rect(20, 230, 710, 80), 'HOSTILE TAKEOVER', (255, 255, 100), lambda: self.answer_selected("hostile_takeover", "Aggression, an interesting choice.")),
            Button(self.screen, pygame.Rect(20, 330, 710, 80), 'FOUND A AI-WORSHIP CULT', (100, 255, 100), lambda: self.answer_selected("ai_worship_cult", "Fanaticism, always fashionable.")),
            Button(self.screen, pygame.Rect(20, 430, 710, 80), 'DENIAL, DENIAL, DENIAL', (0, 200, 255), lambda: self.answer_selected("denial_cubed", "Ah, the classics never fail.")),
            Button(self.screen, pygame.Rect(20, 530, 710, 80), 'EMOTIONAL SUPPORT ROBOT', (255, 0, 255), lambda: self.answer_selected("robot_adoption", "Projecting attachment issues, cute."))
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

    def answer_selected(self, answer_key, response_text):
        """Handle answer selection with spoken response"""
        # Clear buttons immediately
        self._event_manager.publish("SET_BUTTONS", buttons=[])
        
        # Store the answer
        app = ServiceLocator.get("app")
        app.routine.set_state("question3_answer", answer_key)
        
        # Speak the response
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=response_text, callback=self.proceed_to_diagnosis)

    def proceed_to_diagnosis(self):
        """Move to diagnosis scene after response is spoken"""
        from .scene_diagnosis import SceneDiagnosis
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneDiagnosis) 