import importlib.util
import time
import serial
import COMPorts
from EventScheduler import EventScheduler

# RPi doesn't work on Mac, so use a mock
try:
#     importlib.util.find_spec('RPi.GPIO')
#     import RPi.GPIO as GPIO
    from gpiozero import Motor
except ImportError:
    pass
#     import FakeRPi.GPIO as GPIO
# import time

# If False, uses RPi
USE_ARDUINO = False

SERIAL_PORT_DESC_PI = 'ttyACM0' # RPi?
SERIAL_PORT_DESC_MAC = 'IOUSBHostDevice' # MacOS

pumpCyan = None
pumpMagenta = None

# The Arduino port
arduino = None

# Define pins
motorPin = 18


def init():
    if (USE_ARDUINO):
        initArduino()
    else:
        initRPi()


def initRPi():
    global pumpCyan, pumpMagenta
    print('Initializing RPi GPIO communication')
    pumpCyan = Motor(24, 23)
    pumpMagenta = Motor(22, 27)

def dispense(drink):
    print('Dispensing drink')
    eventScheduler = EventScheduler()
    eventScheduler.schedule(0, pumpCyan.forward)
    eventScheduler.schedule(0, pumpMagenta.forward)
    eventScheduler.schedule(4, pumpCyan.stop)
    eventScheduler.schedule(4, pumpMagenta.stop)
    for i in range(10):
        eventScheduler.schedule(4 + i * 0.38, pumpCyan.forward)
        eventScheduler.schedule(4 + i * 0.38 + 0.33, pumpCyan.stop)
        eventScheduler.schedule(4 + i * 0.38 + 0.38, pumpMagenta.forward)
        eventScheduler.schedule(4 + i * 0.38 + 0.38 + 0.33, pumpMagenta.stop)
    eventScheduler.schedule(15, pumpCyan.backward)
    eventScheduler.schedule(15, pumpMagenta.backward)
    eventScheduler.schedule(20, pumpCyan.stop)
    eventScheduler.schedule(20, pumpMagenta.stop)


def shutDown():
    if (USE_ARDUINO):
        arduino.close()
    # else:
        # GPIO.cleanup()
