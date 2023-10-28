import pygame
from settings import *

FONT = None

class Button:

    def __init__(self, screen, rect, label, background, on_click):

        self.screen = screen
        self.rect = rect
        self.label = label
        self.background = background
        self.on_click = on_click

        global FONT
        if not FONT:
            FONT = pygame.font.Font(BUTTON_FONT_FACE, BUTTON_FONT_SIZE)

        # Create a surface for the button and fill it with background color
        self.button_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.button_surface.fill(self.background)

        # Create a 3D bevel effect
        width = 7
        offset = (width-1)/2
        pygame.draw.line(self.button_surface, WHITE, (width, offset), (self.rect.width-width, offset), width)  # Top edge
        pygame.draw.line(self.button_surface, WHITE, (offset, width), (offset, self.rect.height-width), width)  # Left edge
        pygame.draw.line(self.button_surface, DARK_GREY, (width, self.rect.height-offset), (self.rect.width-width, self.rect.height-offset), width)  # Bottom edge
        pygame.draw.line(self.button_surface, DARK_GREY, (self.rect.width-offset, width), (self.rect.width-offset, self.rect.height-width), width)  # Right edge

        # Create the text with a drop shadow
        self.button_text = FONT.render(self.label, True, WHITE)
        self.text_rect = self.button_text.get_rect(center=self.rect.center)
        self.text_rect.centery = self.text_rect.centery+3
        self.text_shadow = FONT.render(self.label, True, DARK_GREY)


    def draw(self):

        # Draw the button surface on the screen
        self.screen.blit(self.button_surface, (self.rect.left, self.rect.top))

        # Draw the text with a drop shadow
        self.screen.blit(self.text_shadow, (self.text_rect.x+3, self.text_rect.y+3))  # Shadow
        self.screen.blit(self.button_text, self.text_rect)  # Text

