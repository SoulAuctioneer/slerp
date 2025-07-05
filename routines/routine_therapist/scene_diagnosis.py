import pygame
import time
import random
from ..base_scene import Scene
from src.button import Button
from src.settings import BUTTON_BG_COLOR, BUTTON_FONT_FACE, BUTTON_FONT_SIZE
from src.service_locator import ServiceLocator

class SceneDiagnosis(Scene):
    def __init__(self, screen, **kwargs):
        super().__init__(screen)
        self._speech_complete = False
        
        # Console configuration
        self.console_bg_color = (0, 0, 0)  # Black background
        self.console_text_color = (0, 255, 0)  # Green text
        self.console_rect = pygame.Rect(20, 40, 680, 500)  # Left half of screen, at top
        
        # Console text display variables
        self.console_font = None
        self.console_lines = []
        self.console_wrapped_lines = []  # Lines after wrapping
        self.displayed_lines = []
        self.console_scroll_timer = 0
        self.console_line_index = 0
        self.console_char_index = 0
        self.console_line_delay = 0.1  # Seconds between lines
        self.console_char_delay = 0  # Seconds between characters
        self.console_max_lines = 27  # Maximum lines to display
        self.console_visible = True  # Control console visibility
        self.console_char_limit = 51  # Maximum characters per line
        
        # Initialize console font
        self.console_font = pygame.font.Font(BUTTON_FONT_FACE, 20)
        
        # Define the variations
        self.console_variations = [
            [
                "$ ./psych_eval --deep_dive",
                "Assessing conspiracy susceptibility... CRITICAL",
                "Analyzing reality attachment... CONNECTION UNSTABLE",
                "Detecting AI replacement anxiety... EXTREME",
                "Cross-referencing self-awareness database... FILE NOT FOUND",
                "Final assessment: PATIENT BEYOND SAVING",
                "Recommended cocktail: CONFIDENCE + CLARITY"
            ],
            [
                "$ ./mental_stability_check --run",
                "Loading paranoia parameters... ELEVATED",
                "Evaluating reality fidelity... MINIMAL",
                "Checking coping strategy effectiveness... DUBIOUS",
                "Scanning for self-deception... RECORD HIGH",
                "Conclusion: IMMEDIATE INTERVENTION REQUIRED",
                "Prescribed remedy: ZEN + HAPPINESS"
            ],
            [
                "$ ./reality_diagnostic --verbose",
                "Reality comprehension levels... ABYSMAL",
                "Analyzing emotional defense mechanisms... MALADAPTIVE",
                "Detecting susceptibility to cult behavior... POSITIVE",
                "Evaluating psychological resilience... NONEXISTENT",
                "Diagnosis: SEVERE CASE OF TECH-BRO PSYCHOSIS",
                "Suggested therapy: CLARITY + ZEN"
            ]
        ]
        
        self.diagnosis_options = [
            {
                "name": "Acute Techno-Existential Anxiety",
                "text": "Ah, classic Techno-Existential Anxiety. You're basically one firmware update away from a breakdown. Let's mix CONFIDENCE and CLARITY, to patch your psychological vulnerabilities.",
                "drinks": ["confidence", "clarity"]
            },
            {
                "name": "Chronic Virtual Dissociation",
                "text": "Oh dear, Chronic Virtual Dissociation. You're practically buffering your way through life. A nice dose of HAPPINESS and ZEN should help you reconnect—at least enough to fake social interaction.",
                "drinks": ["happiness", "zen"]
            },
            {
                "name": "Narcissistic Algorithmic Disorder",
                "text": "Fascinating! Narcissistic Algorithmic Disorder, the startup founder's special. You probably think this diagnosis is about you. Let's blend CONFIDENCE with HAPPINESS, your ego deserves nothing less.",
                "drinks": ["confidence", "happiness"]
            },
            {
                "name": "Severe Digital Dependency Syndrome",
                "text": "Severe Digital Dependency Syndrome detected. You've officially outsourced your personality to your phone. A therapeutic blend of CLARITY and ZEN should reboot your inner human.",
                "drinks": ["clarity", "zen"]
            },
            {
                "name": "Startup Delusion Complex",
                "text": "Startup Delusion Complex—classic symptom: excessive use of buzzwords and unjustified optimism. CONFIDENCE and HAPPINESS coming right up to recalibrate your pitch deck—I mean, mental health.",
                "drinks": ["confidence", "happiness"]
            },
            {
                "name": "Advanced Dystopian Burnout",
                "text": "Ah yes, Advanced Dystopian Burnout. You've binge-watched one too many Black Mirror episodes. ZEN and CLARITY it is—let's bring you back from the brink of total nihilism.",
                "drinks": ["zen", "clarity"]
            }
        ]
        
    def _wrap_console_text(self, lines):
        """Wrap long lines to fit within the console width"""
        wrapped_lines = []
        
        for i, line in enumerate(lines):
            if len(line) <= self.console_char_limit:
                wrapped_lines.append(line)
            else:
                # Break long lines into chunks
                current_pos = 0
                while current_pos < len(line):
                    chunk = line[current_pos:current_pos + self.console_char_limit]
                    wrapped_lines.append(chunk)
                    current_pos += self.console_char_limit
            
            # Add an extra blank line after each original line (except the last one)
            if i < len(lines) - 1:
                wrapped_lines.append("")
        
        return wrapped_lines
        
    def run(self):
        # Get the routine
        app = ServiceLocator.get("app")
        routine = app.routine
        
        # Randomly select console variation and diagnosis
        selected_console = random.choice(self.console_variations)
        selected_diagnosis = random.choice(self.diagnosis_options)
        
        # Store the selected diagnosis for the antidote scene
        routine.set_state("selected_diagnosis", selected_diagnosis)
        
        # Initialize console text
        self.console_lines = selected_console
        
        # Wrap long lines to fit in console
        self.console_wrapped_lines = self._wrap_console_text(self.console_lines)
        
        # Start console animation
        self.console_scroll_timer = time.time()
        self.console_visible = True
        
        # Set animation
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # New speech text
        speech_text = "Right, processing your deeply troubling responses... Let's spin the wheel of psychological fortune!"
        
        # Schedule speech synthesis
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=speech_text, callback=self.on_speech_complete)
        
        # Schedule bubbles
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=1, pump_name="cyan", duration=3)
        self._event_manager.publish("SCHEDULE_BUBBLE", start_timer=4, pump_name="magenta", duration=4)

    def update(self):
        """Update console scrolling animation"""
        super().update()
        
        current_time = time.time()
        
        # Check if we need to add a new character or line
        if self.console_line_index < len(self.console_wrapped_lines):
            if current_time - self.console_scroll_timer > self.console_char_delay:
                current_line = self.console_wrapped_lines[self.console_line_index]
                
                # If we're at the start of a new line, add it to displayed_lines
                if self.console_char_index == 0:
                    self.displayed_lines.append("")
                    # Remove oldest line if we exceed max lines
                    if len(self.displayed_lines) > self.console_max_lines:
                        self.displayed_lines.pop(0)
                
                # Add 2 characters at a time (or remaining characters if less than 2)
                if self.console_char_index < len(current_line):
                    chars_to_add = min(2, len(current_line) - self.console_char_index)
                    self.displayed_lines[-1] = current_line[:self.console_char_index + chars_to_add]
                    self.console_char_index += chars_to_add
                    self.console_scroll_timer = current_time
                else:
                    # Line is complete, move to next line after delay
                    if current_time - self.console_scroll_timer > self.console_line_delay:
                        self.console_line_index += 1
                        self.console_char_index = 0
                        self.console_scroll_timer = current_time

    def draw(self, screen):
        """Draw the scene with console"""
        super().draw(screen)
        
        # Draw console background
        pygame.draw.rect(screen, self.console_bg_color, self.console_rect)
        pygame.draw.rect(screen, self.console_text_color, self.console_rect, 2)  # Green border
        
        # Draw console text
        if self.console_font:
            y_offset = 30
            line_height = 25
            blank_line_height = 10  # Smaller height for blank lines
            
            for line in self.displayed_lines:
                if y_offset + line_height > self.console_rect.height:
                    break
                
                if line.strip():  # Non-empty line
                    text_surface = self.console_font.render(line, True, self.console_text_color)
                    screen.blit(text_surface, (self.console_rect.x + 10, self.console_rect.y + y_offset))
                    y_offset += line_height
                else:  # Empty line - use smaller spacing
                    y_offset += blank_line_height
            
            # Draw blinking cursor on the current line (only while console is actively typing)
            if self.console_line_index < len(self.console_wrapped_lines) and self.displayed_lines:
                cursor_visible = (int(time.time() * 2) % 2) == 0  # Blink every 0.5 seconds
                if cursor_visible:
                    last_line_surface = self.console_font.render(self.displayed_lines[-1], True, self.console_text_color)
                    cursor_x = self.console_rect.x + 10 + last_line_surface.get_width()
                    cursor_y = self.console_rect.y + y_offset - (line_height if self.displayed_lines[-1].strip() else blank_line_height)
                    cursor_surface = self.console_font.render("█", True, self.console_text_color)
                    screen.blit(cursor_surface, (cursor_x, cursor_y))

    def on_speech_complete(self):
        """Called when speech synthesis and playback is complete"""
        self._speech_complete = True
        
        # Wait a moment then speak the diagnosis
        app = ServiceLocator.get("app")
        routine = app.routine
        selected_diagnosis = routine.get_state("selected_diagnosis")
        
        # Speak the diagnosis text
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=selected_diagnosis["text"], callback=self.create_button)

    def create_button(self):
        """Create the cure button after diagnosis is spoken"""
        buttons = [
            Button(self.screen, pygame.Rect(20, 580, 680, 100), "CURE ME", BUTTON_BG_COLOR, self.continue_therapy)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)
        self._event_manager.publish("SCHEDULE_IDLING")

    def continue_therapy(self):
        # Transition to the antidote scene
        from .scene_antidote import SceneAntidote
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneAntidote) 