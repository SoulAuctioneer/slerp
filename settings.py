# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Fullscreen or windowed
IS_FULLSCREEN = True

# Background image
BG_IMAGE = "assets/background-logo-1280x720.png"

# Caption if windowed
WINDOW_CAPTION = 'Slerp the Slushmaster'

# Colors
WHITE = (255, 255, 255)
NEON_BLUE = (50, 50, 255)
DARK_BLUE = (25, 25, 128)
DARK_GREY = (32, 32, 32)

# Font properties
BUTTON_FONT_SIZE = 48
BUTTON_FONT_FACE = 'assets/PeaberryMono.ttf'

# Pump GPIO pins
PUMP_CYAN_OUT = 24
PUMP_CYAN_IN = 23
PUMP_MAGENTA_OUT = 22
PUMP_MAGENTA_IN = 27
PUMP_YELLOW_OUT = 8
PUMP_YELLOW_IN = 0
PUMP_EXTRA_OUT = 0
PUMP_EXTRA_IN = 0

# Max number of squirts of liquid that can be produced from each pump per drink
DISPENSER_MAX_SQUIRTS = 10
# Time to prime liquids from reservoir to top of collector
DISPENSER_PRIME_DURATION = 5
# Time to pump for a single squirt
DISPENSER_SQUIRT_DURATION = 0.38
# Time to rest between squirts
DISPENSER_SQUIRT_REST_DURATION = 0.33
# Time to wait after all squirts are done before sucking back
DISPENSER_SUCK_WAIT_DURATION = 12
# Time to suck back into reservoir
DISPENSER_SUCK_DURATION = 5