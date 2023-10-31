from gpiozero import Motor, Device, PWMOutputDevice
from gpiozero.pins.mock import MockFactory, MockPWMPin
import event_scheduler
import platform
from settings import *

class Dispenser:

    def __init__(self):

        print('Initializing GPIO communication')

        # Mock if not on raspberry pi
        if not platform.system() == 'Linux' and not platform.machine() == 'aarch64':
            print('gpiozero is disabled')
            Device.pin_factory = MockFactory(pin_class=MockPWMPin)

        self.event_scheduler = event_scheduler.EventScheduler()

        # Initialize the pump pins
        self.pumps = {
            'cyan': {'motor': Motor(PUMP_CYAN_OUT, PUMP_CYAN_IN), 'prime_duration': PUMP_CYAN_PRIME_DURATION, 'speed': PWMOutputDevice(PUMP_CYAN_SPEED)},
            'magenta': {'motor': Motor(PUMP_MAGENTA_OUT, PUMP_MAGENTA_IN), 'prime_duration': PUMP_MAGENTA_PRIME_DURATION, 'speed': PWMOutputDevice(PUMP_MAGENTA_SPEED)},
            'yellow': {'motor': Motor(PUMP_YELLOW_OUT, PUMP_YELLOW_IN), 'prime_duration': PUMP_YELLOW_PRIME_DURATION, 'speed': PWMOutputDevice(PUMP_YELLOW_SPEED)},
            'transparent': {'motor': Motor(PUMP_TRANSPARENT_OUT, PUMP_TRANSPARENT_IN), 'prime_duration': PUMP_TRANSPARENT_PRIME_DURATION, 'speed': PWMOutputDevice(PUMP_TRANSPARENT_SPEED)}
        }
        for pump_name, pump in self.pumps.items():
            self.set_speed(pump_name, 1.0)

    # Dispense a drink with the given amounts of Cyan / Magenta / Yellow / Transparent, from 0 to max
    # TODO: Create a drink class with the squirt amounts, name, and button color
    # TODO: Add a callback when done dispensing, or simply a return value that's the number of seconds it'll take to pour
    def dispense(self, drink):

        print('Dispensing drink')

         # Tracks timing of all events in seconds
        timer = 0

        # Prime all liquids to the top of the collector
        for pump_name, pump in self.pumps.items():
            self.forward(pump_name)
            self.event_scheduler.schedule(pump['prime_duration'], lambda: self.stop(pump_name))
        timer += max(PUMP_CYAN_PRIME_DURATION, PUMP_MAGENTA_PRIME_DURATION, PUMP_YELLOW_PRIME_DURATION, PUMP_TRANSPARENT_PRIME_DURATION)

        # Pause for a second
        timer += 1

        # Iterate up to max times, scheduling liquid to pump if more of its color is still needed
        for i in range(DISPENSER_MAX_SQUIRTS):
            for pump_name, amount in {'cyan': drink.cmyt[0], 'magenta': drink.cmyt[1], 'yellow': drink.cmyt[2], 'transparent': drink.cmyt[3]}.items():
                if amount > i:
                    self.event_scheduler.schedule(timer, lambda: self.forward(pump_name))
                    timer += DISPENSER_SQUIRT_DURATION
                    self.event_scheduler.schedule(timer, lambda: self.stop(pump_name))
                    timer += DISPENSER_SQUIRT_REST_DURATION

        # Suck all the liquids back into the reservoir
        timer += DISPENSER_SUCK_WAIT_DURATION
        for pump_name, pump in self.pumps.items():
            self.event_scheduler.schedule(timer, lambda: self.backward(pump_name))

        # Stop sucking
        timer += DISPENSER_SUCK_DURATION
        for pump_name, pump in self.pumps.items():
            self.event_scheduler.schedule(timer, lambda: self.stop(pump_name))

        return timer

    # Run the pump in reverse for the given duration to bubble the reservoir
    def bubble(self, pump_name, duration):
        self.backward(pump_name)
        self.event_scheduler.schedule(duration, lambda: self.stop(pump_name))

    # Run the pump forward for 3 seconds then backwards
    def test(self, pump_name):
        self.set_speed(pump_name, 0.5)
        self.forward(pump_name)
        self.event_scheduler.schedule(7.4, lambda: self.backward(pump_name))
        self.event_scheduler.schedule(13, lambda: self.stop(pump_name))

    def forward(self, pump_name):
         self.pumps[pump_name]['motor'].forward()
    
    def backward(self, pump_name):
        self.pumps[pump_name]['motor'].backward()

    def stop(self, pump_name):
        self.pumps[pump_name]['motor'].stop()

    def set_speed(self, pump_name, speed):
        self.pumps[pump_name]['speed'].value = speed

    # Execute any events due
    def update(self):
        self.event_scheduler.execute_due()
