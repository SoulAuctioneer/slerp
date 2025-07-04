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

    def trigger_if_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.on_click(*self.args)

    def draw(self, screen):

        if self.is_invisible:
            return

        # Draw the pre-rendered button surface on the screen
        screen.blit(self.button_surface, (self.rect.left, self.rect.top))

        # Draw the full-resolution text
        if self.label:
            screen.blit(self.text_shadow, self.shadow_rect)
            screen.blit(self.button_text, self.text_rect)
