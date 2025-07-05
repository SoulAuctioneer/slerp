#!/bin/bash

cd ~/slerp
# Set the SDL_AUDIODEV environment variable to force Pygame/SDL to use the
# USB audio device (card 3, device 0 from `aplay -l`).
# This is needed because the script is run with sudo, which doesn't use the
# current user's audio settings. 'plughw:1,0' is a common
export SDL_AUDIODEV=plughw:3,0
sudo -E .venv/bin/python ./main.py
