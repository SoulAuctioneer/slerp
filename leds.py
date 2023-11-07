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
        #r,g,b acts as the last instruction
        r = 0
        g = 0
        b = 0
        #current values can move around r,g,b
        while True:
            try:
                r, g, b = queue.get_nowait()                      
                                                                
                
            except:
                pass
            # JUST FILL ALL THE LEDS
            self.pixels.fill((r, g, b))
            #PLAY
            #We just use the last rgb val
            # if r == 0 and g == 0 and b == 0:
            #     self.pixels.fill((0, 0, 0))
            #     pass
            # else:
            #     while rmin + gmin + bmin < r + g + b:
            #         for i in range(self.num_pixels):
            #             pixel_index = ((i * 256) // self.num_pixels) + rmin + gmin + bmin
            #             self.pixels[pixel_index] = (rmin,gmin,bmin)
            #             self.pixels.show()
            #         if (rmin <= r):
            #             rmin = rmin + 1
            #         if (gmin <= g):
            #             gmin = gmin + 1
            #         if (bmin <= b):
            #             bmin = bmin + 1
            self.pixels.show()
            time.sleep(0.01)
            

            


class Leds:
    q : Queue = None
    leds: _leds = None

    def __init__(self):
        global queue
        if Leds.q is None:
            Leds.q = queue
            Leds.leds = _leds()
            p = multiprocessing.Process(target=Leds.leds.run, name="LEDS", args=())
            p.start()        

