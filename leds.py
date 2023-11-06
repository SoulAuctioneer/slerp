import asyncio
import concurrent.futures
import event_scheduler
import time
import board
import neopixel
import multiprocessing 

class Leds:

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
        self.ORDER = neopixel.GRB

        self.pixels = neopixel.NeoPixel(
            pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER
        )

        print('Initializing LEDs')

        self.event_scheduler = event_scheduler.EventScheduler()

    def stop(self):
        for j in range(self.num_pixels):
            self.pixels[j] = (0,0,0)
        self.pixels.show()

    def run(self):
        def wheel(pos):
            # Input a value 0 to 255 to get a color value.
            # The colours are a transition r - g - b - back to r.
            if pos < 0 or pos > 255:
                r = g = b = 0
            elif pos < 85:
                r = int(pos * 3)
                g = int(255 - pos * 3)
                b = 0
            elif pos < 170:
                pos -= 85
                r = int(255 - pos * 3)
                g = 0
                b = int(pos * 3)
            else:
                pos -= 170
                r = 0
                g = int(pos * 3)
                b = int(255 - pos * 3)
            return (r, g, b) if self.ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


        def rainbow_cycle(wait):
            for j in range(255):
                for i in range(self.num_pixels):
                    pixel_index = (i * 256 // self.num_pixels) + j
                    self.pixels[i] = wheel(pixel_index & 255)
                self.pixels.show()
                time.sleep(wait)


        while True:
            # Comment this line out if you have RGBW/GRBW NeoPixels
            self.pixels.fill((255, 0, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((255, 0, 0, 0))
            self.pixels.show()
            time.sleep(1)

            # Comment this line out if you have RGBW/GRBW NeoPixels
            self.pixels.fill((0, 255, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 255, 0, 0))
            self.pixels.show()
            time.sleep(1)

            # Comment this line out if you have RGBW/GRBW NeoPixels
            self.pixels.fill((0, 0, 255))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 0, 255, 0))
            self.pixels.show()
            time.sleep(1)

            rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

async def test():
    loop = asyncio.get_running_loop()
    l = Leds()
    # Run in a custom process pool:
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, l.run)

ledz = Leds()
def test2():
    p = multiprocessing.Process(target=ledz.run, name="LEDS", args=())
    p.start()
    return p

#asyncio.run(test())
p = test2()
p.join(3)
ledz.stop()
p.terminate()