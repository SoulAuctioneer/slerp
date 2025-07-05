import pygame
from ..base_scene import Scene
from src.button import Button
from src.service_locator import ServiceLocator
from src.settings import DEBUG_INSTANT_BUTTONS, SCREEN_WIDTH, WHITE, SUBTITLE_FONT_SIZE
from src.text_utils import draw_wrapped_text, get_font

class SceneQuestion2(Scene):

    # Question 2 speech text
    SPEECH_TEXT = "And how would you describe your relationship status with reality?"
    QUESTION_TEXT = "How would you describe your relationship status with reality?"

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
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=1, pump_name='yellow', duration=3)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=4, pump_name='transparent', duration=4)

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
            Button(self.screen, pygame.Rect(20, 170, 710, 80), 'IN A COMMITTED DELUSION', (255, 100, 100), lambda: self.answer_selected("committed_delusion", "At least you're loyal.")),
            Button(self.screen, pygame.Rect(20, 270, 710, 80), 'EMOTIONALLY UNAVAILABLE', (100, 100, 255), lambda: self.answer_selected("emotionally_unavailable", "Avoidance is your love language.")),
            Button(self.screen, pygame.Rect(20, 370, 710, 80), 'IT\'S COMPLICATED', (255, 255, 100), lambda: self.answer_selected("its_complicated", "Ambiguity, your favorite defense.")),
            Button(self.screen, pygame.Rect(20, 470, 710, 80), 'POLYAMOROUS WITH VR', (100, 255, 100), lambda: self.answer_selected("polyamorous_vr", "Exploring virtual infidelity, bold.")),
            Button(self.screen, pygame.Rect(20, 570, 710, 80), 'CASUALLY GASLIGHTING', (0, 200, 255), lambda: self.answer_selected("casually_gaslighting", "Consistency isn't your strong suit."))
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
        app.routine.set_state("question2_answer", answer_key)
        
        # Speak the response
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=response_text, callback=self.proceed_to_question3)
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)

    def proceed_to_question3(self):
        """Move to question 3 after response is spoken"""
        from .scene_question3 import SceneQuestion3
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneQuestion3) 

    def draw(self, screen):
        if self.show_question_text:
            text_rect = pygame.Rect(15, 50, 720, 150)
            draw_wrapped_text(screen, self.QUESTION_TEXT, text_rect, self.font, WHITE, center_x=True) 