import pygame
import os
import sys

# Add the 'lib' directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from src.app import App

if __name__ == '__main__':
    pygame.init()
    app = App()
    app.run()
    app.shut_down() 