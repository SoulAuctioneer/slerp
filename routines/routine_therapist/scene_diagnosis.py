import pygame
import time
from ..base_scene import Scene
from src.button import Button
from src.settings import BUTTON_BG_COLOR, BUTTON_FONT_FACE, BUTTON_FONT_SIZE
from src.service_locator import ServiceLocator

class SceneDiagnosis(Scene):
    def __init__(self, screen, diagnosis_key=None, **kwargs):
        super().__init__(screen)
        self.diagnosis_key = diagnosis_key
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
        self.console_line_delay = 0.1  # Seconds between lines (reduced from 0.8)
        self.console_char_delay = 0  # Seconds between characters (reduced from 0.05)
        self.console_max_lines = 27  # Maximum lines to display (adjusted for 500px height)
        self.console_visible = True  # Control console visibility
        self.console_char_limit = 51  # Maximum characters per line (configurable)
        
        # Initialize console font
        self.console_font = pygame.font.Font(BUTTON_FONT_FACE, 20)
        
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
        # Get the routine and fetch diagnosis configuration
        app = ServiceLocator.get("app")
        routine = app.routine
        
        if not self.diagnosis_key:
            # If no diagnosis key provided, get it from routine state
            self.diagnosis_key = routine.get_state("current_diagnosis")
        
        if not self.diagnosis_key:
            # Fallback - shouldn't happen but just in case
            self.diagnosis_key = "default"
        
        # Get the diagnosis config
        diagnosis_config = routine.get_config("diagnoses", {}).get(self.diagnosis_key, {})
        
        # Initialize console text
        self.console_lines = diagnosis_config.get("console_text", [
            "$ diagnostic_scanner --unknown-error",
            "No diagnosis configuration found...",
            "Running default troubleshooting protocol..."
        ])
        
        # Wrap long lines to fit in console
        self.console_wrapped_lines = self._wrap_console_text(self.console_lines)
        
        # Start console animation
        self.console_scroll_timer = time.time()
        self.console_visible = True
        
        # Set animation
        self._event_manager.publish("SET_SLERP_ANIMATION", animation_name="talking", loops=0)
        
        # Get speech text
        speech_text = diagnosis_config.get("speech_text", "I don't know what's wrong with you.")
        
        # Schedule speech synthesis
        self._event_manager.publish("SYNTHESIZE_SPEECH", text=speech_text, callback=self.on_speech_complete)
        
        # Schedule bubbles based on config
        bubbles = diagnosis_config.get("bubbles", [])
        for bubble in bubbles:
            self._event_manager.publish("SCHEDULE_BUBBLE", 
                                      start_timer=bubble.get("start_timer", 1),
                                      pump_name=bubble.get("pump_name", "cyan"),
                                      duration=bubble.get("duration", 3))

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
        
        # Keep the console visible - don't hide it
        
        # Create continue button below the console
        buttons = [
            Button(self.screen, pygame.Rect(20, 580, 680, 100), "CURE ME", BUTTON_BG_COLOR, self.continue_therapy)
        ]
        self._event_manager.publish("SET_BUTTONS", buttons=buttons)
        self._event_manager.publish("SCHEDULE_IDLING")

    def continue_therapy(self):
        # Transition to the antidote scene with the diagnosis key
        from .scene_antidote import SceneAntidote
        self._event_manager.publish("CHANGE_SCENE", scene_class=SceneAntidote, diagnosis_key=self.diagnosis_key) 