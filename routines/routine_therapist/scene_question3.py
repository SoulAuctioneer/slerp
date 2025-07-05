import pygame
from ..base_scene import Scene
from src.button import Button
from src.service_locator import ServiceLocator
from src.settings import DEBUG_INSTANT_BUTTONS, SCREEN_WIDTH, WHITE, SUBTITLE_FONT_SIZE
from src.text_utils import draw_wrapped_text, get_font

class SceneQuestion3(Scene):

    # Question 3 speech text
    SPEECH_TEXT = "Finally, what coping mechanism will you use when AI inevitably replaces you?"
    QUESTION_TEXT = "What coping mechanism will you use when AI inevitably replaces you?"
        
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self._speech_complete = False
        self.show_question_text = False
        self.font = get_font(SUBTITLE_FONT_SIZE)

    def run(self):
        # Start speech synthesis
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=self.SPEECH_TEXT, callback=self.on_speech_complete)
        
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
        self.show_question_text = True
        self._event_manager.publish("SCHEDULE_IDLING")

    def create_buttons(self):
        buttons = [
            Button(self.screen, pygame.Rect(20, 120, 710, 80), 'MINDFUL SURRENDER', (255, 100, 100), lambda: self.answer_selected("mindful_surrender", "Zen or just lazy?")),
            Button(self.screen, pygame.Rect(20, 215, 710, 80), 'IRRATIONAL OPTIMISM', (100, 100, 255), lambda: self.answer_selected("overcompensating_optimism", "Delusion masked as hope, charming.")),
            Button(self.screen, pygame.Rect(20, 310, 710, 80), 'HOSTILE TAKEOVER', (255, 255, 100), lambda: self.answer_selected("hostile_takeover", "Aggression, an interesting choice.")),
            Button(self.screen, pygame.Rect(20, 405, 710, 80), 'FOUND A AI-WORSHIP CULT', (100, 255, 100), lambda: self.answer_selected("ai_worship_cult", "Fanaticism, always fashionable.")),
            Button(self.screen, pygame.Rect(20, 500, 710, 80), 'DENIAL, DENIAL, DENIAL', (0, 200, 255), lambda: self.answer_selected("denial_cubed", "Ah, the classics never fail.")),
            Button(self.screen, pygame.Rect(20, 595, 710, 80), 'EMOTIONAL SUPPORT ROBOT', (255, 0, 255), lambda: self.answer_selected("robot_adoption", "Projecting attachment issues, cute."))
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)

    def answer_selected(self, answer_key, response_text):
        """Handle answer selection with spoken response"""
        self.show_question_text = False
        self._event_manager.publish("STOP_AUDIO") # To stop any idling sounds
        # Clear buttons immediately
        self._event_manager.publish("SET_BUTTONS", buttons=[])
        
        # Store the answer
        app = ServiceLocator.get("app")
        app.routine.set_state("question3_answer", answer_key)
        
        # Speak the response
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=response_text, callback=self.proceed_to_diagnosis)
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)

    def proceed_to_diagnosis(self):
        """Move to diagnosis scene after response is spoken"""
        from .scene_diagnosis import SceneDiagnosis
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneDiagnosis) 

    def draw(self, screen):
        if self.show_question_text:
            text_rect = pygame.Rect(15, 50, 720, 150)
            draw_wrapped_text(screen, self.QUESTION_TEXT, text_rect, self.font, WHITE, center_x=True) 