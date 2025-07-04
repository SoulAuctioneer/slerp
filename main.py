import sys
import os

# Add src and lib directories to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import logging
from main_loop import MainLoop
# from leds import Leds
import multiprocessing

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                        handlers=[logging.FileHandler('log.txt', 'w', 'utf-8'),
                                  logging.StreamHandler()])

    # Initialize the looper
    main_loop = MainLoop()

    # Fire up the first page of the narrative
    main_loop.start()

    # Start the main loop running
    main_loop.run()

    # Quit, so shut down the main loop
    main_loop.shut_down() 