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
PUMP_MAGENTA_SPEED = 19
PUMP_YELLOW_OUT = 23
PUMP_YELLOW_IN = 24
PUMP_YELLOW_SPEED = 18
PUMP_TRANSPARENT_OUT = 27
PUMP_TRANSPARENT_IN = 22
PUMP_TRANSPARENT_SPEED = 13

# Time to prime liquids from reservoir to top of collector. Will be different if there's a variance in tube length
PUMP_CYAN_PRIME_DURATION = 4.7
PUMP_MAGENTA_PRIME_DURATION = 5.2
PUMP_YELLOW_PRIME_DURATION = 5.9
PUMP_TRANSPARENT_PRIME_DURATION = 6.2

# Time to pump for a single squirt
DISPENSER_SQUIRT_DURATION = 0.25
# Time to rest between squirts
DISPENSER_SQUIRT_REST_DURATION = 0.05
# Time to wait after all squirts are done before sucking back
DISPENSER_SUCK_WAIT_DURATION = 3
