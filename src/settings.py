import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Active routine
ACTIVE_ROUTINE = "routine_therapist"

# Debug settings
DEBUG_INSTANT_BUTTONS = False

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Fullscreen or windowed
IS_FULLSCREEN = True

# Background image
BG_IMAGE = "assets/background-logo-1280x720.png"
BG_IMAGE_SYMBOL = "assets/background-symbol.png"

# Music tracks
MUSIC = ["music1", "music2", "music3", "music4"]
PLAY_MUSIC = False
SNORE_LOUD = True

# Caption if windowed
WINDOW_CAPTION = 'Slerp the Slushmaster'

# Colors
WHITE = (255, 255, 255)
NEON_BLUE = (50, 50, 255)
DARK_BLUE = (25, 25, 128)
DARK_GREY = (32, 32, 32)
BUTTON_BG_COLOR = (255, 0, 255)

# Hidden debug button size
BUTTON_DEBUG_SIZE = 100

# Font properties
BUTTON_FONT_SIZE = 48
BUTTON_FONT_FACE = 'assets/PeaberryMono.ttf'

# Pump GPIO pins
# Bottom Right - Looking from rear
PUMP_TRANSPARENT_OUT = 14 # Blue
PUMP_TRANSPARENT_IN = 15 # Green
PUMP_TRANSPARENT_SPEED = 18 # Purple

# Top Right - Looking from rear
PUMP_MAGENTA_OUT = 17 # Yellow # NOTE FLIPPED
PUMP_MAGENTA_IN = 27 # Orange # NOTE FLIPPED
PUMP_MAGENTA_SPEED = 13 # Brown

# Bottom Left - Looking from rear
PUMP_YELLOW_OUT = 25 # Yellow 
PUMP_YELLOW_IN = 24 # Orange
PUMP_YELLOW_SPEED = 12 # Brown

# Top Left - Looking from rear
PUMP_CYAN_OUT = 11 # Blue # NOTE FLIPPED
PUMP_CYAN_IN = 9 # Green # NOTE FLIPPED
PUMP_CYAN_SPEED = 19 # Purple

# Time to prime liquids from reservoir to top of collector. Will be different if there's a variance in tube length
PUMP_CYAN_PRIME_DURATION = 3.85
PUMP_MAGENTA_PRIME_DURATION = 4.7
PUMP_YELLOW_PRIME_DURATION = 4.25
PUMP_TRANSPARENT_PRIME_DURATION = 4.85

# Time to pump for a single squirt
DISPENSER_SQUIRT_DURATION = 0.25
# Time to rest between squirts
DISPENSER_SQUIRT_REST_DURATION = 0.05
# Time to wait after all squirts are done before sucking back
DISPENSER_SUCK_WAIT_DURATION = 3

# Time to wait for user input before resetting
IDLE_TIMEOUT = 20

# --- ElevenLabs TTS Settings ---
# API key is loaded from .env file in project root
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = "gipH2sj2YZY4V4JjuONC" # "3jbSUx3cT1r6mnw1ePpf"
ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"
TTS_CACHE_DIR = "assets/tts_cache"

# --- Subtitle Settings ---
SUBTITLES_ENABLED = True
SUBTITLE_FONT_SIZE = 30
SUBTITLE_COLOR = (255, 255, 255)  # White
SUBTITLE_BACKGROUND_COLOR = (0, 0, 0, 64)  # Semi-transparent black
SUBTITLE_PADDING = 5
SUBTITLE_Y_OFFSET = 35  # Distance from bottom of screen
SUBTITLE_SCROLL_SPEED = 13  # pixels per frame
SUBTITLE_SCROLL_START_DELAY = 0  # frames to wait before starting scroll (1.25 seconds at 24fps)

# --- Retro Typewriter Settings ---
SUBTITLE_MAX_CHARS_PER_CHUNK = 68  # Maximum characters per subtitle chunk
SUBTITLE_TYPEWRITER_SPEED = 30  # Characters per second for typewriter effect
SUBTITLE_CHUNK_PAUSE_DURATION = 0.3  # Seconds to pause between chunks
