import asyncio
import concurrent.futures
import event_scheduler
import time
import board
import neopixel
import multiprocessing
from multiprocessing import Queue

queue = Queue()

class _leds:

    def __init__(self):

        # On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
        # Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
        pixel_pin = board.D18

        # On a Raspberry pi, use this instead, not all pins are supported
        # pixel_pin = board.D18

        # The number of NeoPixels
        self.num_pixels = 300

        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        self.ORDER = neopixel.RGB

        self.pixels = neopixel.NeoPixel(
            pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
        )

        print('Initializing LEDs')

        self.event_scheduler = event_scheduler.EventScheduler()

    def run(self):
        global queue
        while True:
            r, g, b = queue.get(True, None)                        
            # Comment this line out if you have RGBW/GRBW NeoPixels
            self.pixels.fill((r, g, b))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((255, 0, 0, 0))
            self.pixels.show()
            time.sleep(0.1)

            


class Leds:
    q : Queue = None
    leds: _leds = None

    def __init__(self, q: Queue):
        if Leds.q is None:
            Leds.q = Queue()
            Leds.leds = _leds()
            p = multiprocessing.Process(target=Leds.leds.run, name="LEDS", args=())
            p.start()        

