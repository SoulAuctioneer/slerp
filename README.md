# Slerp the SlushMaster

Slerp the SlushMaster is an interactive art installation running on a Raspberry Pi. It features a narrative-driven user interface built with Pygame that guides the user through a humorous story with a slushie-dispensing supercomputer named Slerp. The application controls a physical slushie machine via GPIO pins to dispense different colored liquids based on user choices.

## Features

*   **Interactive Narrative:** A multi-scene story with branching choices, presented through on-screen text, character animations, and voice-over audio.
*   **Physical Integration:** Controls up to four liquid pumps using `gpiozero` to create custom-mixed drinks.
*   **Pygame-based UI:** A graphical user interface with animated sprites, custom fonts, and interactive buttons.
*   **Event-Driven Architecture:** Uses a custom event scheduler for precise timing of animations, audio cues, and hardware actions.
*   **Configurable:** Key parameters like GPIO pin assignments, screen settings, and pump timings are easily configurable in a central settings file.
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

*   `main.py`: The main entry point of the application. It sets up the environment and starts the main loop.
*   `src/`: This directory contains all the main source code for the application.
    *   `main_loop.py`: The core of the application. It manages the game state, event loop, and acts as a context for the different scenes.
    *   `scenes/`: This directory holds the logic for each individual scene in the narrative.
    *   `settings.py`: Contains all the global configuration constants, such as screen dimensions, GPIO pin numbers, and asset paths.
    *   `dispenser.py`: Handles all communication with the GPIO pins to control the liquid pumps.
    *   `slerp_sprite.py`: Manages the loading and animation of the Slerp character sprites.
    *   `audio.py`: Manages loading and playback of all audio files.
    *   `speech_synthesiser.py`: Uses the ElevenLabs API to generate speech audio clips from text.
    *   `button.py`: A UI component for creating interactive buttons.
    *   `drink.py`: A simple data class to define the properties of each drink.
    *   `event_scheduler.py`: A simple scheduler to trigger functions after a specified delay.
*   `lib/`: Contains third-party library files.
*   `tests/`: Contains scripts for testing hardware components.
*   `assets/`: Contains all the media for the project, including images, fonts, and audio files.

## Configuration

Most of the application's behavior can be customized in `settings.py`:

*   `IS_FULLSCREEN`: Set to `True` for fullscreen or `False` for a windowed display.
*   `SCREEN_WIDTH`, `SCREEN_HEIGHT`: The dimensions of the display.
*   `PUMP_*` constants: The GPIO pin numbers and timing characteristics for each pump. These **must** be configured correctly for your hardware.
*   `PLAY_MUSIC`, `SNORE_LOUD`: Toggles for background music and specific sound effects.

## Admin Panel

There is a hidden admin panel for debugging and testing. To access it, click on the **bottom-right corner** of the screen.

The admin panel provides the following options:
*   **RESTART:** Returns to the very first scene.
*   **DRINKS SCREEN:** Jumps directly to the drink selection scene.
*   **TEST [COLOR]:** Runs a specific pump for a short duration.
*   **TEST PRIMING:** Runs the full priming and un-priming sequence for all pumps.
*   **EXIT:** Shuts down the application.
