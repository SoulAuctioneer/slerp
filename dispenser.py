from gpiozero import Motor, Device
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
            'cyan': {'motor': Motor(PUMP_CYAN_OUT, PUMP_CYAN_IN), 'prime_duration': PUMP_CYAN_PRIME_DURATION},
            'magenta': {'motor': Motor(PUMP_MAGENTA_OUT, PUMP_MAGENTA_IN), 'prime_duration': PUMP_MAGENTA_PRIME_DURATION},
            'yellow': {'motor': Motor(PUMP_YELLOW_OUT, PUMP_YELLOW_IN), 'prime_duration': PUMP_YELLOW_PRIME_DURATION},
            'transparent': {'motor': Motor(PUMP_TRANSPARENT_OUT, PUMP_TRANSPARENT_IN), 'prime_duration': PUMP_TRANSPARENT_PRIME_DURATION}
        }

    # Dispense a drink with the given amounts of Cyan / Magenta / Yellow / Transparent, from 0 to max
    # TODO: Create a drink class with the squirt amounts, name, and button color
    # TODO: Add a callback when done dispensing, or simply a return value that's the number of seconds it'll take to pour
    def dispense(self, drink):

        print('Dispensing drink')

         # Tracks timing of all events in seconds
        timer = 0

        # Prime all liquids to the top of the collector
        for color, pump in self.pumps.items():
            pump['motor'].forward()
            self.event_scheduler.schedule(pump['prime_duration'], pump['motor'].stop)
        timer += max(PUMP_CYAN_PRIME_DURATION, PUMP_MAGENTA_PRIME_DURATION, PUMP_YELLOW_PRIME_DURATION, PUMP_TRANSPARENT_PRIME_DURATION)

        # Pause for a second
        timer += 1

        # Iterate up to max times, scheduling liquid to pump if more of its color is still needed
        for i in range(DISPENSER_MAX_SQUIRTS):
            for color, amount in {'cyan': drink.cmyt[0], 'magenta': drink.cmyt[1], 'yellow': drink.cmyt[2], 'transparent': drink.cmyt[3]}.items():
                if amount > i:
                    self.event_scheduler.schedule(timer, self.pumps[color]['motor'].forward)
                    timer += DISPENSER_SQUIRT_DURATION
                    self.event_scheduler.schedule(timer, self.pumps[color]['motor'].stop)
                    timer += DISPENSER_SQUIRT_REST_DURATION

        # Suck all the liquids back into the reservoir
        timer += DISPENSER_SUCK_WAIT_DURATION
        for color, pump in self.pumps.items():
            self.event_scheduler.schedule(timer, pump['motor'].backward)

        # Stop sucking
        timer += DISPENSER_SUCK_DURATION
        for color, pump in self.pumps.items():
            self.event_scheduler.schedule(timer, pump['motor'].stop)

        print(timer)
        return timer

    # Run the pump in reverse for the given duration to bubble the reservoir
    def bubble(self, pump_name, duration):
        pump = self.pumps[pump_name]
        pump['motor'].backward()
        self.event_scheduler.schedule(duration, pump['motor'].stop)

    # Execute any events due
    def update(self):
        self.event_scheduler.execute_due()
