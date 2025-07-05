import pygame
import pygame.time
import re
from .service_locator import ServiceLocator
from .settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_FONT_FACE,
    SUBTITLES_ENABLED, SUBTITLE_FONT_SIZE, SUBTITLE_COLOR,
    SUBTITLE_BACKGROUND_COLOR, SUBTITLE_PADDING,
    SUBTITLE_Y_OFFSET, SUBTITLE_MAX_CHARS_PER_CHUNK,
    SUBTITLE_TYPEWRITER_SPEED, SUBTITLE_CHUNK_PAUSE_DURATION,
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
        self.should_show_subtitles = True
        
        # Chunking state
        self.text_chunks = []
        self.current_chunk_index = 0
        self.current_chunk_text = ""
        
        # Typewriter state
        self.typewriter_progress = 0  # Characters to show in current chunk
        self.typewriter_timer = 0.0  # Time accumulator for typewriter effect
        self.chars_per_frame = SUBTITLE_TYPEWRITER_SPEED / 24.0  # Characters per frame at 24fps
        
        # Timing state
        self.chunk_start_time = 0
        self.chunk_display_duration = 0
        self.chunk_pause_start_time = 0
        self.is_in_chunk_pause = False
        
        # Speech timing tracking
        self.speech_start_time = 0
        self.speech_duration = 0
        
        # Subtitle styling - use configurable settings
        self.enabled = SUBTITLES_ENABLED
        self.font_size = SUBTITLE_FONT_SIZE
        self.font_color = SUBTITLE_COLOR
        self.background_color = SUBTITLE_BACKGROUND_COLOR
        self.padding = SUBTITLE_PADDING
        self.max_chars_per_chunk = SUBTITLE_MAX_CHARS_PER_CHUNK
        self.typewriter_speed = SUBTITLE_TYPEWRITER_SPEED
        self.chunk_pause_duration = SUBTITLE_CHUNK_PAUSE_DURATION
        
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
        
        # Calculate timing for chunks
        self._calculate_chunk_timing()
        
        # Start first chunk
        self._start_chunk(0)
    
    def show_subtitles(self, text):
        """Display subtitles for the given text"""
        self.current_text = text
        self.is_visible = True
        
        # Split text into chunks
        self.text_chunks = self._split_into_chunks(text)
        
        # Reset state
        self.current_chunk_index = 0
        self.current_chunk_text = ""
        self.typewriter_progress = 0
        self.typewriter_timer = 0.0
        self.chunk_start_time = 0
        self.is_in_chunk_pause = False
    
    def _split_into_chunks(self, text):
        """Split text into readable chunks, preferring word boundaries"""
        if len(text) <= self.max_chars_per_chunk:
            return [text]
        
        chunks = []
        words = text.split()
        current_chunk = ""
        
        for word in words:
            # Check if adding this word would exceed the limit
            test_chunk = current_chunk + (" " if current_chunk else "") + word
            
            if len(test_chunk) <= self.max_chars_per_chunk:
                current_chunk = test_chunk
            else:
                # Current chunk is full, start a new one
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = word
                else:
                    # Single word is too long, we need to break it
                    chunks.append(word[:self.max_chars_per_chunk])
                    remaining = word[self.max_chars_per_chunk:]
                    while remaining:
                        chunk_size = min(len(remaining), self.max_chars_per_chunk)
                        chunks.append(remaining[:chunk_size])
                        remaining = remaining[chunk_size:]
                    current_chunk = ""
        
        # Add the last chunk if there's content
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _calculate_chunk_timing(self):
        """Calculate how long each chunk should be displayed"""
        if not self.text_chunks or self.speech_duration <= 0:
            return
        
        # Calculate total time available for chunks (minus pause time)
        total_pause_time = (len(self.text_chunks) - 1) * self.chunk_pause_duration * 1000
        available_time = self.speech_duration - total_pause_time
        
        # Distribute time proportionally based on chunk length
        total_chars = sum(len(chunk) for chunk in self.text_chunks)
        
        if total_chars > 0:
            # Base time per character
            time_per_char = available_time / total_chars
            
            # Calculate display duration for each chunk
            self.chunk_durations = []
            for chunk in self.text_chunks:
                # Time for typewriter effect
                typewriter_time = len(chunk) / self.typewriter_speed * 1000
                # Time for reading (proportional to chunk length)
                reading_time = len(chunk) * time_per_char
                # Use the longer of the two, with a minimum display time
                chunk_duration = max(typewriter_time + 500, reading_time, 1000)  # Minimum 1 second
                self.chunk_durations.append(chunk_duration)
        else:
            # Fallback: equal time for all chunks
            time_per_chunk = available_time / len(self.text_chunks)
            self.chunk_durations = [time_per_chunk] * len(self.text_chunks)
    
    def _start_chunk(self, chunk_index):
        """Start displaying a specific chunk"""
        if chunk_index >= len(self.text_chunks):
            self.hide_subtitles()
            return
        
        self.current_chunk_index = chunk_index
        self.current_chunk_text = self.text_chunks[chunk_index]
        self.typewriter_progress = 0
        self.typewriter_timer = 0.0
        self.chunk_start_time = pygame.time.get_ticks()
        self.chunk_display_duration = self.chunk_durations[chunk_index]
        self.is_in_chunk_pause = False
    
    def _start_chunk_pause(self):
        """Start pause between chunks"""
        self.is_in_chunk_pause = True
        self.chunk_pause_start_time = pygame.time.get_ticks()
        self.current_chunk_text = ""  # Clear text during pause
    
    def hide_subtitles(self):
        """Hide the current subtitles"""
        self.is_visible = False
        self.current_text = ""
        self.text_chunks = []
        self.current_chunk_index = 0
        self.current_chunk_text = ""
        self.typewriter_progress = 0
        self.typewriter_timer = 0.0
        self.chunk_start_time = 0
        self.is_in_chunk_pause = False
        self.speech_start_time = 0
        self.speech_duration = 0
        self.should_show_subtitles = True
    
    def update(self):
        """Update subtitle state - called each frame"""
        if not self.enabled or not self.is_visible:
            return
        
        # Check if speech has finished
        if self.speech_duration > 0:
            current_time = pygame.time.get_ticks()
            speech_elapsed = current_time - self.speech_start_time
            
            if speech_elapsed >= self.speech_duration + 1000:  # 1 second buffer
                self.hide_subtitles()
                return
        
        # Handle chunk transitions and typewriter effect
        if self.is_in_chunk_pause:
            # Check if pause is over
            current_time = pygame.time.get_ticks()
            pause_elapsed = current_time - self.chunk_pause_start_time
            
            if pause_elapsed >= self.chunk_pause_duration * 1000:
                # Start next chunk
                self._start_chunk(self.current_chunk_index + 1)
        
        elif self.current_chunk_text:
            # Handle typewriter effect
            self.typewriter_timer += self.chars_per_frame
            new_progress = int(self.typewriter_timer)
            
            if new_progress > self.typewriter_progress:
                self.typewriter_progress = min(new_progress, len(self.current_chunk_text))
            
            # Check if chunk display time is over
            current_time = pygame.time.get_ticks()
            chunk_elapsed = current_time - self.chunk_start_time
            
            if chunk_elapsed >= self.chunk_display_duration:
                # Move to next chunk or start pause
                if self.current_chunk_index + 1 < len(self.text_chunks):
                    self._start_chunk_pause()
                else:
                    # All chunks done
                    self.hide_subtitles()
    
    def draw(self, screen):
        """Draw typewriter subtitles on the screen"""
        if not self.enabled:
            return
        
        # Always draw the background area to clear any old text
        subtitle_height = self.font_size + (self.padding * 2)
        subtitle_width = SCREEN_WIDTH
        bg_x = 0
        bg_y = self.subtitle_y - self.padding
        
        if self.is_visible and self.current_chunk_text and not self.is_in_chunk_pause:
            # Get the text to display (up to typewriter progress)
            display_text = self.current_chunk_text[:self.typewriter_progress]
            
            if display_text:
                # Create background surface with transparency
                background_surface = pygame.Surface((subtitle_width, subtitle_height))
                background_surface.fill(self.background_color[:3])  # RGB only
                background_surface.set_alpha(self.background_color[3])  # Alpha
                screen.blit(background_surface, (bg_x, bg_y))
                
                # Render the text
                text_surface = self.font.render(display_text, True, self.font_color)
                
                # Left-align the text to prevent movement during typewriter effect
                text_x = self.padding
                text_y = bg_y + self.padding
                
                screen.blit(text_surface, (text_x, text_y))
        else:
            # Clear the subtitle area by redrawing the background image
            if self.background_image:
                # Extract the portion of the background image that corresponds to the subtitle area
                bg_rect = pygame.Rect(bg_x, bg_y, subtitle_width, subtitle_height)
                screen.blit(self.background_image, (bg_x, bg_y), bg_rect)
            else:
                # Fallback to solid color if background image not available
                pygame.draw.rect(screen, (32, 32, 32), (bg_x, bg_y, subtitle_width, subtitle_height)) 