import pygame

class Button:
    # Colors
    WHITE = (255, 255, 255)
    NEON_BLUE = (50, 50, 255)
    DARK_BLUE = (25, 25, 128)
    DARK_GREY = (32, 32, 32)

    # Font properties
    button_font_size = 48

    def __init__(self, screen, button_rect, button_string='NOTHING HERE', background=(255, 0, 255)):
        self.screen = screen
        self.button_rect = button_rect
        self.button_string = button_string
        self.background = background
        self.button_font = pygame.font.Font('assets/PeaberryMono.ttf', self.button_font_size)

    def draw(self):
        # Create a surface for the button and fill it with background color
        button_surface = pygame.Surface((self.button_rect.width, self.button_rect.height))
        button_surface.fill(self.background)

        # Create a 3D bevel effect
        width = 7
        offset = (width-1)/2
        pygame.draw.line(button_surface, self.WHITE, (width, offset), (self.button_rect.width-width, offset), width)  # Top edge
        pygame.draw.line(button_surface, self.WHITE, (offset, width), (offset, self.button_rect.height-width), width)  # Left edge
        pygame.draw.line(button_surface, self.DARK_GREY, (width, self.button_rect.height-offset), (self.button_rect.width-width, self.button_rect.height-offset), width)  # Bottom edge
        pygame.draw.line(button_surface, self.DARK_GREY, (self.button_rect.width-offset, width), (self.button_rect.width-offset, self.button_rect.height-width), width)  # Right edge

        # Draw the button surface on the screen
        self.screen.blit(button_surface, (self.button_rect.left, self.button_rect.top))

        # Draw the text with a drop shadow
        button_text = self.button_font.render(self.button_string, True, self.WHITE)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        text_rect.centery = text_rect.centery+3
        text_shadow = self.button_font.render(self.button_string, True, self.DARK_GREY)
        self.screen.blit(text_shadow, (text_rect.x+3, text_rect.y+3))  # Shadow
        self.screen.blit(button_text, text_rect)  # Text

