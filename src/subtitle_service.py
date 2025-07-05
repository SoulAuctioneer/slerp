import pygame
import pygame.time
from .service_locator import ServiceLocator
from .settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_FONT_FACE,
    SUBTITLES_ENABLED, SUBTITLE_FONT_SIZE, SUBTITLE_COLOR,
    SUBTITLE_BACKGROUND_COLOR, SUBTITLE_PADDING,
    SUBTITLE_Y_OFFSET, SUBTITLE_SCROLL_SPEED, SUBTITLE_SCROLL_START_DELAY,
    BG_IMAGE
)

class SubtitleService:
    def __init__(self):
        self._event_manager = ServiceLocator.get("event_manager")
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        
        # Subscribe to speech events
        self._event_manager.subscribe("SYNTHESIZE_SPEECH", self.on_speech_start)
        self._event_manager.subscribe("SPEECH_STARTED", self.on_speech_started)
        self._event_manager.subscribe("STOP_SPEECH", self.hide_subtitles)
        
        # Subtitle state
        self.current_text = ""
        self.is_visible = False
        self.subtitle_duration = 0
        
        # Scrolling state
        self.scroll_x = 0
        self.scroll_speed = SUBTITLE_SCROLL_SPEED
        self.text_width = 0
        self.scroll_start_delay = SUBTITLE_SCROLL_START_DELAY
        self.scroll_delay_counter = 0
        self.has_scrolled_off_screen = False
        
        # Speech timing tracking
        self.speech_start_time = 0
        self.speech_duration = 0
        self.should_show_subtitles = True
        
        # Subtitle styling - use configurable settings
        self.enabled = SUBTITLES_ENABLED
        self.font_size = SUBTITLE_FONT_SIZE
        self.font_color = SUBTITLE_COLOR
        self.background_color = SUBTITLE_BACKGROUND_COLOR
        self.padding = SUBTITLE_PADDING
        self.max_width = SCREEN_WIDTH - (self.padding * 2)
        
        # Position subtitles at bottom of screen
        self.subtitle_y = SCREEN_HEIGHT - SUBTITLE_Y_OFFSET
        
        # Initialize font
        try:
            self.font = pygame.font.Font(BUTTON_FONT_FACE, self.font_size)
        except (pygame.error, FileNotFoundError):
            print("Custom font not found, using default font")
            self.font = pygame.font.Font(None, self.font_size)
        
        # Load background image for clearing
        try:
            self.background_image = pygame.image.load(BG_IMAGE)
        except (pygame.error, FileNotFoundError):
            print("Background image not found, using solid color fallback")
            self.background_image = None
    
    def on_speech_start(self, text, callback=None, show_subtitles=True, **kwargs):
        """Handle speech synthesis start - show subtitles"""
        self.should_show_subtitles = show_subtitles
        
        if not self.enabled or not show_subtitles:
            return
            
        self.show_subtitles(text)
    
    def on_speech_started(self, duration, **kwargs):
        """Handle actual speech start with exact duration from TTS service"""
        if not self.enabled or not self.should_show_subtitles:
            return
            
        # Record exact speech timing
        self.speech_start_time = pygame.time.get_ticks()
        self.speech_duration = duration * 1000  # Convert to milliseconds
    
    def show_subtitles(self, text):
        """Display subtitles for the given text"""
        self.current_text = text
        self.is_visible = True
        
        # Reset scrolling state
        self.scroll_x = SCREEN_WIDTH  # Start from right edge
        self.scroll_delay_counter = 0
        self.has_scrolled_off_screen = False
        
        # Calculate text width for scrolling
        if self.font:
            self.text_width = self.font.size(text)[0]
        else:
            self.text_width = len(text) * (self.font_size * 0.6)  # Rough estimate
    
    def hide_subtitles(self):
        """Hide the current subtitles"""
        self.is_visible = False
        self.current_text = ""
        # Reset scrolling state
        self.scroll_x = 0
        self.scroll_delay_counter = 0
        self.has_scrolled_off_screen = False
        self.text_width = 0
        # Reset speech timing
        self.speech_start_time = 0
        self.speech_duration = 0
        self.should_show_subtitles = True
    
    def draw(self, screen):
        """Draw scrolling subtitles on the screen"""
        if not self.enabled:
            return
        
        # Always draw the background area to clear any old text
        subtitle_height = self.font_size + (self.padding * 2)
        subtitle_width = SCREEN_WIDTH
        bg_x = 0
        bg_y = self.subtitle_y - self.padding
        
        if self.is_visible and self.current_text:
            # Create background surface with transparency
            background_surface = pygame.Surface((subtitle_width, subtitle_height))
            background_surface.fill(self.background_color[:3])  # RGB only
            background_surface.set_alpha(self.background_color[3])  # Alpha
            screen.blit(background_surface, (bg_x, bg_y))
            
            # Render the text
            text_surface = self.font.render(self.current_text, True, self.font_color)
            
            # Create a clipping surface to prevent text from showing outside subtitle area
            clip_surface = pygame.Surface((subtitle_width, subtitle_height))
            clip_surface.fill((0, 0, 0))  # Fill with black (will be transparent)
            clip_surface.set_colorkey((0, 0, 0))  # Make black transparent
            
            # Draw text on clipping surface at scroll position
            text_y = self.padding
            clip_surface.blit(text_surface, (self.scroll_x, text_y))
            
            # Draw the clipped text to the screen
            screen.blit(clip_surface, (0, bg_y))
        else:
            # Clear the subtitle area by redrawing the background image
            if self.background_image:
                # Extract the portion of the background image that corresponds to the subtitle area
                bg_rect = pygame.Rect(bg_x, bg_y, subtitle_width, subtitle_height)
                screen.blit(self.background_image, (bg_x, bg_y), bg_rect)
            else:
                # Fallback to solid color if background image not available
                pygame.draw.rect(screen, (32, 32, 32), (bg_x, bg_y, subtitle_width, subtitle_height))
    
    def update(self):
        """Update subtitle state - called each frame"""
        if not self.enabled or not self.is_visible or not self.current_text:
            return
        
        # Check if speech has finished (with exact timing)
        if self.speech_duration > 0:
            current_time = pygame.time.get_ticks()
            speech_elapsed = current_time - self.speech_start_time
            
            # Hide subtitles when speech finishes (with small buffer)
            if speech_elapsed >= self.speech_duration + 1000:  # 1 second buffer
                self.hide_subtitles()
                return
        
        # Handle scrolling animation
        if self.scroll_delay_counter < self.scroll_start_delay:
            # Still in initial delay period
            self.scroll_delay_counter += 1
        elif not self.has_scrolled_off_screen:
            # Start scrolling left
            self.scroll_x -= self.scroll_speed
            
            # Check if text has completely scrolled off screen
            if self.scroll_x + self.text_width < 0:
                self.has_scrolled_off_screen = True
                # Hide subtitles when done scrolling
                self.hide_subtitles()
        
        # If text is shorter than screen width, center it instead of scrolling
        if self.text_width <= SCREEN_WIDTH:
            self.scroll_x = (SCREEN_WIDTH - self.text_width) // 2 