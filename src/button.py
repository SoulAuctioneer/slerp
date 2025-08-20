import pygame
from .settings import *

FONT = None

class Button:

    def __init__(self, screen, rect, label, background, on_click, *args):

        self.rect = rect
        self.label = label
        self.background = background
        self.on_click = on_click
        self.args = args
        
        # Touch responsiveness improvements
        self.touch_padding = 10  # Extra pixels around button for touch detection
        self.is_pressed = False  # Track if button is currently being pressed
        self.last_trigger_time = 0  # For debouncing

        # Buttons without label and background color are invisible
        self.is_invisible = not self.label and not self.background
        if self.is_invisible:
            return

        # Create a low-resolution surface for a pixelated effect
        scale = 4
        low_res_width = self.rect.width // scale
        low_res_height = self.rect.height // scale
        low_res_surface = pygame.Surface((low_res_width, low_res_height), pygame.SRCALPHA)

        # Drawing parameters for the low-res surface
        border_radius = 3  # 12 / 4
        bevel = 1          # 4 / 4
        width, height = low_res_width, low_res_height

        # 1. Shadow
        shadow_rect = pygame.Rect(bevel, bevel, width - bevel, height - bevel)
        pygame.draw.rect(low_res_surface, DARK_GREY, shadow_rect, border_radius=border_radius)

        # 2. Highlight
        highlight_rect = pygame.Rect(0, 0, width - bevel, height - bevel)
        pygame.draw.rect(low_res_surface, WHITE, highlight_rect, border_radius=border_radius)

        # 3. Button Face
        face_rect = pygame.Rect(bevel, bevel, width - (2 * bevel), height - (2 * bevel))
        pygame.draw.rect(low_res_surface, self.background, face_rect, border_radius=border_radius)

        # Scale up the surface to create the final pixelated button
        self.button_surface = pygame.transform.scale(low_res_surface, (self.rect.width, self.rect.height))
        
        # Create pressed version with darker colors
        pressed_surface = low_res_surface.copy()
        # Darken the button face for pressed state
        pressed_color = tuple(max(0, c - 50) for c in self.background)
        pygame.draw.rect(pressed_surface, pressed_color, face_rect, border_radius=border_radius)
        self.button_surface_pressed = pygame.transform.scale(pressed_surface, (self.rect.width, self.rect.height))

        # Create the text at full resolution
        if self.label:
            global FONT
            if not FONT:
                FONT = pygame.font.Font(BUTTON_FONT_FACE, BUTTON_FONT_SIZE)
            
            # Render text with a drop shadow
            self.text_shadow = FONT.render(self.label, True, DARK_GREY)
            self.shadow_rect = self.text_shadow.get_rect(center=self.rect.center)
            self.shadow_rect.move_ip(2, 2)

            self.button_text = FONT.render(self.label, True, WHITE)
            self.text_rect = self.button_text.get_rect(center=self.rect.center)

    def get_touch_rect(self):
        """Get expanded rectangle for better touch detection"""
        return pygame.Rect(
            self.rect.x - self.touch_padding,
            self.rect.y - self.touch_padding,
            self.rect.width + (self.touch_padding * 2),
            self.rect.height + (self.touch_padding * 2)
        )
    
    def handle_mouse_down(self, pos):
        """Handle mouse/touch down event"""
        if self.get_touch_rect().collidepoint(pos):
            self.is_pressed = True
            return True
        return False
    
    def handle_mouse_up(self, pos):
        """Handle mouse/touch up event - triggers the button if still over it"""
        current_time = pygame.time.get_ticks()
        
        # Debouncing: prevent multiple triggers within 200ms
        if current_time - self.last_trigger_time < 200:
            self.is_pressed = False
            return False
            
        if self.is_pressed and self.get_touch_rect().collidepoint(pos):
            self.is_pressed = False
            self.last_trigger_time = current_time
            self.on_click(*self.args)
            return True
        
        self.is_pressed = False
        return False
    
    def trigger_if_clicked(self, pos):
        """Legacy method for backward compatibility"""
        if self.rect.collidepoint(pos):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_trigger_time >= 200:  # Debouncing
                self.last_trigger_time = current_time
                self.on_click(*self.args)

    def draw(self, screen):

        if self.is_invisible:
            return

        # Draw the appropriate button surface (pressed or normal)
        if self.is_pressed:
            screen.blit(self.button_surface_pressed, (self.rect.left, self.rect.top))
        else:
            screen.blit(self.button_surface, (self.rect.left, self.rect.top))

        # Draw the full-resolution text
        if self.label:
            screen.blit(self.text_shadow, self.shadow_rect)
            screen.blit(self.button_text, self.text_rect)
