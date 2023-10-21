import importlib.util
import serial
import COMPorts

# RPi doesn't work on Mac, so use a mock
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

import time


ports = COMPorts.get_com_ports()
for port in ports:
    print(port.device)
    print(port.description)

# If False, uses RPi
USE_ARDUINO = True

# TODO: Check if this can change across OS
SERIAL_PORT_DESC = 'ttyACM0'

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
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motorPin, GPIO.OUT)


def initArduino():
    global arduino
    # Initialize Arduino communication
    print('Initializing Arduino communication')
    port_name = COMPorts.get_device_by_description(SERIAL_PORT_DESC)
    print(port_name)
    arduino = serial.Serial(port=port_name, baudrate=9600, timeout=5)
    time.sleep(1)  # Seems like it needs a moment before you can start sending commands


def dispense(drink):
    if (USE_ARDUINO):
        if drink == 'drink1':
            arduino.write(b'CMD_DRINK1')
    else:
        # Turn on the motor
        GPIO.output(motorPin, GPIO.HIGH)
        time.sleep(5)  # Let the motor run for 1 second

        # Turn off the motor
        GPIO.output(motorPin, GPIO.LOW)


def shutDown():
    if (USE_ARDUINO):
        arduino.close()
    else:
        GPIO.cleanup()
