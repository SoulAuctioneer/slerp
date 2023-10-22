import importlib.util
import time
import serial
import COMPorts
from gpiozero import Motor

# RPi doesn't work on Mac, so use a mock
# try:
#     importlib.util.find_spec('RPi.GPIO')
#     import RPi.GPIO as GPIO
# except ImportError:
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
    pumpCyan = Motor(23, 24)
    pumpMagenta = Motor(27, 22)


def initArduino():
    global arduino
    # Initialize Arduino communication
    print('Initializing Arduino communication')
    port_name = COMPorts.get_device_by_description(SERIAL_PORT_DESC_MAC)
    if (port_name is None):
        port_name = COMPorts.get_device_by_description(SERIAL_PORT_DESC_PI)
    print(port_name)
    arduino = serial.Serial(port=port_name, baudrate=9600, timeout=5)
    time.sleep(1)  # Seems like it needs a moment before you can start sending commands


def dispense(drink):
    print('Dispensing drink')
    if (USE_ARDUINO):
        if drink == 'drink1':
            try:
                arduino.write(b'CMD_DRINK1')
            except:
                print('Failed to write to the arduino -- is it connected?')
    else:
        pumpCyan.forward()
        pumpMagenta.forward()
        time.sleep(5)
        while True:
            pumpCyan.forward()
            pumpMagenta.stop()
            time.sleep(0.33)
            pumpCyan.stop()
            pumpMagenta.forward()
            time.sleep(0.33)

        pumpCyan.stop()


def shutDown():
    if (USE_ARDUINO):
        arduino.close()
    # else:
        # GPIO.cleanup()
