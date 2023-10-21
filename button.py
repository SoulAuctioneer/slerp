import sys
import pygame

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
NEON_BLUE = (50, 50, 255)
DARK_BLUE = (25, 25, 128)
DARK_GREY = (32, 32, 32)

# Font properties
button_font_size = 48
button_font = pygame.font.Font('assets/PeaberryMono.ttf', button_font_size)

def draw_button(screen, button_rect, button_string='NOTHING HERE', background=(255, 0, 255)):

    # Create a surface for the button and fill it with magenta color
    button_surface = pygame.Surface((button_rect.width, button_rect.height))
    button_surface.fill(background)  # Magenta color

    # Create a 3D bevel effect
    width = 7
    offset = (width-1)/2
    pygame.draw.line(button_surface, WHITE, (width, offset), (button_rect.width-width, offset), width)  # Top edge
    pygame.draw.line(button_surface, WHITE, (offset, width), (offset, button_rect.height-width), width)  # Left edge
    pygame.draw.line(button_surface, DARK_GREY, (width, button_rect.height-offset), (button_rect.width-width, button_rect.height-offset), width)  # Bottom edge
    pygame.draw.line(button_surface, DARK_GREY, (button_rect.width-offset, width), (button_rect.width-offset, button_rect.height-width), width)  # Right edge

    # Draw the button surface on the screen
    screen.blit(button_surface, (button_rect.left, button_rect.top))

    # Draw the text with a drop shadow
    button_text = button_font.render(button_string, True, WHITE)
    text_rect = button_text.get_rect(center=button_rect.center)
    text_rect.centery = text_rect.centery+3
    text_shadow = button_font.render(button_string, True, DARK_BLUE)
    screen.blit(text_shadow, (text_rect.x+3, text_rect.y+3))  # Shadow
    screen.blit(button_text, text_rect)  # Text
