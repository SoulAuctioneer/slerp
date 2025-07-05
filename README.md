# Slerp the SlushMaster

Slerp the SlushMaster is an interactive art installation running on a Raspberry Pi. It features a narrative-driven user interface built with Pygame that guides the user through a humorous story with a slushie-dispensing supercomputer named Slerp. The application controls a physical slushie machine via GPIO pins to dispense different colored liquids based on user choices.

## Features

*   **Interactive Narrative:** A multi-scene story with branching choices, presented through on-screen text, character animations, and voice-over audio.
*   **Physical Integration:** Controls up to four liquid pumps using `gpiozero` to create custom-mixed drinks.
*   **Pygame-based UI:** A graphical user interface with animated sprites, custom fonts, and interactive buttons.
*   **Event-Driven Architecture:** Uses a custom event scheduler for precise timing of animations, audio cues, and hardware actions.
*   **Intelligent Subtitles:** Automatic scrolling subtitles synchronized with speech synthesis, with configurable styling and optional per-speech control.
*   **Configurable:** Key parameters like GPIO pin assignments, screen settings, pump timings, and subtitle appearance are easily configurable in a central settings file.
*   **Admin Panel:** A hidden debug panel provides administrative functions for testing and restarting the experience.

## Hardware Setup

This project is designed to run on a **Raspberry Pi** connected to a slushie dispensing machine. The machine is expected to have four pumps controlled by the Raspberry Pi's GPIO pins.

The specific GPIO pin mappings for each pump (cyan, magenta, yellow, transparent) are defined in `settings.py`. You will need to adjust these values to match your hardware setup.

```python
# settings.py - Example Pump Configuration
# Bottom Right - Looking from rear
PUMP_TRANSPARENT_OUT = 14 # Blue
PUMP_TRANSPARENT_IN = 15 # Green
PUMP_TRANSPARENT_SPEED = 18 # Purple
# ... and so on for other pumps
```

## Software Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SoulAuctioneer/slerp
    cd slerp
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Once the setup is complete, you can run the application with:

```bash
python3 main.py
```

The application will launch in fullscreen mode by default (this can be changed in `settings.py`).

## Project Structure

The codebase is organized into several modules and directories:

*   `main.py`: The main entry point of the application. It initializes the Service Locator and starts the main application loop.
*   `src/`: This directory contains all the main source code for the application.
    *   `app.py`: The core of the application. It manages the game state, event loop, and orchestrates the different routines and scenes.
    *   `settings.py`: Contains all the global configuration constants, such as screen dimensions, GPIO pin numbers, and asset paths.
    *   `service_locator.py`: A simple implementation of the Service Locator pattern that provides global access to shared services like `audio`, `event_manager`, etc.
    *   `scene_manager.py`: Manages the loading, unloading, and transitioning between different scenes.
    *   `event_manager.py`: A simple pub/sub event manager to decouple different parts of the application.
    *   `event_scheduler.py`: A simple scheduler to trigger functions after a specified delay.
    *   `dispenser.py`: Handles all communication with the GPIO pins to control the liquid pumps.
    *   `slerp_sprite.py`: Manages the loading and animation of the Slerp character sprites.
    *   `audio.py`: Manages loading and playback of all audio files.
    *   `speech_synthesiser.py`: Uses the ElevenLabs API to generate speech audio clips from text.
    *   `tts_service.py`: Integrates speech synthesis with the event system and provides exact audio duration.
    *   `subtitle_service.py`: Manages automatic scrolling subtitles synchronized with speech synthesis.
    *   `button.py`: A UI component for creating interactive buttons.
    *   `drink.py`: A simple data class to define the properties of each drink.
*   `routines/`: This directory contains the different narrative paths or "routines" that the user can experience. Each routine is a collection of scenes.
    *   `base_routine.py`: A base class for all routines.
    *   `base_scene.py`: A base class for all scenes.
    *   `routine_ascend/`: An example routine directory, containing the scenes for that specific narrative.
*   `lib/`: Contains third-party library files.
*   `tests/`: Contains scripts for testing hardware components.
*   `assets/`: Contains all the media for the project, including images, fonts, and audio files.

## Subtitle System

The application features an intelligent subtitle system that automatically displays scrolling text synchronized with speech synthesis. The system is designed to be completely decoupled from individual scenes, requiring no changes to existing code.

### How It Works

*   **Automatic Activation:** Subtitles automatically appear when any scene publishes a `SYNTHESIZE_SPEECH` event
*   **Precise Timing:** Uses exact audio duration from the TTS service (no estimation)
*   **Smart Scrolling:** Long text scrolls horizontally from right to left; short text centers on screen
*   **Automatic Cleanup:** Subtitles disappear when speech ends or scrolling completes
*   **Scene Independence:** Subtitles clear automatically when scenes change

### Usage in Scenes

By default, all speech synthesis includes subtitles:

```python
# This will show subtitles automatically
self._event_manager.publish("SYNTHESIZE_SPEECH", text="Hello world!", callback=self.on_speech_complete)
```

To disable subtitles for specific speech (e.g., internal thoughts, background audio):

```python
# This will play TTS but hide subtitles
self._event_manager.publish("SYNTHESIZE_SPEECH", text="Secret message", show_subtitles=False, callback=self.on_speech_complete)
```

### Technical Details

*   **Event-Driven:** Integrates seamlessly with the existing event system
*   **Frame-Based Timing:** Uses reliable frame-based timing instead of schedulers
*   **Background Clearing:** Properly clears old text by redrawing the background image
*   **Configurable Styling:** All visual aspects controlled via `settings.py`

## Configuration

Most of the application's behavior can be customized in `settings.py`:

*   `IS_FULLSCREEN`: Set to `True` for fullscreen or `False` for a windowed display.
*   `SCREEN_WIDTH`, `SCREEN_HEIGHT`: The dimensions of the display.
*   `PUMP_*` constants: The GPIO pin numbers and timing characteristics for each pump. These **must** be configured correctly for your hardware.
*   `PLAY_MUSIC`, `SNORE_LOUD`: Toggles for background music and specific sound effects.

### Subtitle Configuration

*   `SUBTITLES_ENABLED`: Set to `False` to disable subtitles entirely.
*   `SUBTITLE_FONT_SIZE`: Font size for subtitle text (default: 36).
*   `SUBTITLE_COLOR`: RGB color tuple for subtitle text (default: white).
*   `SUBTITLE_BACKGROUND_COLOR`: RGBA color tuple for subtitle background (default: semi-transparent black).
*   `SUBTITLE_PADDING`: Padding around subtitle text in pixels (default: 20).
*   `SUBTITLE_Y_OFFSET`: Distance from bottom of screen in pixels (default: 150).
*   `SUBTITLE_SCROLL_SPEED`: Scrolling speed in pixels per frame (default: 2).
*   `SUBTITLE_SCROLL_START_DELAY`: Frames to wait before starting scroll (default: 30).

## Admin Panel

There is a hidden admin panel for debugging and testing. To access it, click on the **bottom-right corner** of the screen.

The admin panel provides the following options:
*   **RESTART:** Returns to the very first scene.
*   **DRINKS SCREEN:** Jumps directly to the drink selection scene.
*   **TEST [COLOR]:** Runs a specific pump for a short duration.
*   **TEST PRIMING:** Runs the full priming and un-priming sequence for all pumps.
*   **EXIT:** Shuts down the application.
