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

# Hidden debug button size
BUTTON_DEBUG_SIZE = 50

# Font properties
BUTTON_FONT_SIZE = 48
BUTTON_FONT_FACE = 'assets/PeaberryMono.ttf'

# Pump GPIO pins
# Bottom Right - Looking from rear
PUMP_TRANSPARENT_OUT = 14 # Blue
PUMP_TRANSPARENT_IN = 15 # Green
PUMP_TRANSPARENT_SPEED = 18 # Purple
# Top Right - Looking from rear
PUMP_CYAN_OUT = 17 # Yellow
PUMP_CYAN_IN = 27 # Orange
PUMP_CYAN_SPEED = 13 # Brown
# Bottom Left - Looking from rear
PUMP_MAGENTA_OUT = 23 # Blue
PUMP_MAGENTA_IN = 24 # Green
PUMP_MAGENTA_SPEED = 12 # Purple
# Top Left - Looking from rear
PUMP_YELLOW_OUT = 9 # Yellow
PUMP_YELLOW_IN = 11 # Orange
PUMP_YELLOW_SPEED = 19 # Brown

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
