import pygame
from src.settings import WHITE, BUTTON_FONT_FACE, SUBTITLE_FONT_SIZE

def get_font(size=SUBTITLE_FONT_SIZE, bold=False):
    """Gets the default application font."""
    try:
        font = pygame.font.Font(BUTTON_FONT_FACE, size)
    except (pygame.error, FileNotFoundError):
        font = pygame.font.Font(None, size)

    font.set_bold(bold)
    return font

def draw_wrapped_text(screen, text, rect, font, color=WHITE, center_x=True, center_y=False):
    """
    Draws word-wrapped text inside a given pygame.Rect.
    It will automatically wrap words to the next line.
    """
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < rect.width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    total_height = len(lines) * font.get_linesize()

    if center_y:
        start_y = rect.top + (rect.height - total_height) // 2
    else:
        start_y = rect.top

    y = start_y
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        if center_x:
            text_rect.centerx = rect.centerx
        else:
            text_rect.left = rect.left
        text_rect.top = y
        screen.blit(text_surface, text_rect)
        y += font.get_linesize() 