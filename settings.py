# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Fullscreen or windowed
IS_FULLSCREEN = True

# Background image
BG_IMAGE = "assets/background-logo-1280x720.png"

# Music tracks
MUSIC = ["assets/audio/music1.mp3", "assets/audio/music2.mp3", "assets/audio/music3.mp3", "assets/audio/music3.mp3"]

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
PUMP_CYAN_OUT = 7
PUMP_CYAN_IN = 1
PUMP_CYAN_SPEED = 13
PUMP_MAGENTA_OUT = 11
PUMP_MAGENTA_IN = 10
PUMP_MAGENTA_SPEED = 12
PUMP_YELLOW_OUT = 23
PUMP_YELLOW_IN = 24
PUMP_YELLOW_SPEED = 18
PUMP_TRANSPARENT_OUT = 27
PUMP_TRANSPARENT_IN = 22
PUMP_TRANSPARENT_SPEED = 19

# Time to prime liquids from reservoir to top of collector. Will be different if there's a variance in tube length
PUMP_CYAN_PRIME_DURATION = 4.5
PUMP_YELLOW_PRIME_DURATION = 5.5
PUMP_MAGENTA_PRIME_DURATION = 6
PUMP_TRANSPARENT_PRIME_DURATION = 5

# Max number of squirts of liquid that can be produced from each pump per drink
DISPENSER_MAX_SQUIRTS = 10
# Time to pump for a single squirt
DISPENSER_SQUIRT_DURATION = 0.38
# Time to rest between squirts
DISPENSER_SQUIRT_REST_DURATION = 0.2
# Time to wait after all squirts are done before sucking back
DISPENSER_SUCK_WAIT_DURATION = 3
# Time to suck back into reservoir
DISPENSER_SUCK_DURATION = 5
