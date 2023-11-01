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
        for pump_name in self.pumps.keys():
            self.set_speed(pump_name, 1.0)

    # Dispense a drink with the given amounts of Cyan / Magenta / Yellow / Transparent, from 0 to max
    # TODO: Create a drink class with the squirt amounts, name, and button color
    def dispense(self, drink, on_complete=None, *args, **kwargs):

        # Prime all liquids to the top of the collector then wait for a moment, for vibes
        timer = self.prime('forward') + 0.1

        # Iterate up to max times, scheduling liquid to pump if more of its color is still needed
        for i in range(max(drink.cmyt)):
            for pump_name, amount in {'cyan': drink.cmyt[0], 'magenta': drink.cmyt[1], 'yellow': drink.cmyt[2], 'transparent': drink.cmyt[3]}.items():
                if amount > i:
                    self.schedule_forward(timer, pump_name)
                    timer += DISPENSER_SQUIRT_DURATION
                    self.schedule_stop(timer, pump_name)
                    timer += DISPENSER_SQUIRT_REST_DURATION

        # Suck all the liquids back into the reservoir after a pause for chill vibes
        timer += DISPENSER_SUCK_WAIT_DURATION
        timer += self.prime('backward', timer)

        if on_complete:
            self.event_scheduler.schedule(timer, on_complete, *args, **kwargs)

        return timer

    # Prime all liquids either to the top of the collector or back from the collector into the reservoirs
    def prime(self, direction, start_timer=0):

        # Start staggered, finish together
        max_prime_duration = max(pump['prime_duration'] for pump in self.pumps.values())
        for pump_name, pump in self.pumps.items():
            pump_start_timer = start_timer + max_prime_duration - pump['prime_duration']
            self.schedule_set_speed(pump_start_timer, pump_name, 1.0)
            if direction == 'forward':
                self.schedule_forward(pump_start_timer, pump_name)
            else:
                self.schedule_backward(pump_start_timer, pump_name)
            self.schedule_stop(start_timer + max_prime_duration, pump_name)

        return max_prime_duration

    def forward(self, pump_name):
         self.pumps[pump_name]['motor'].forward()
    
    def schedule_forward(self, start_timer, pump_name):
        self.event_scheduler.schedule(start_timer, self.forward, pump_name)

    def backward(self, pump_name):
        self.pumps[pump_name]['motor'].backward()

    def schedule_backward(self, start_timer, pump_name):
        self.event_scheduler.schedule(start_timer, self.backward, pump_name)

    def stop(self, pump_name):
        self.pumps[pump_name]['motor'].stop()

    def schedule_stop(self, start_timer, pump_name):
        self.event_scheduler.schedule(start_timer, self.stop, pump_name)

    def set_speed(self, pump_name, speed):
        self.pumps[pump_name]['speed'].value = speed

    def schedule_set_speed(self, start_timer, pump_name, speed):
        self.event_scheduler.schedule(start_timer, self.set_speed, pump_name, speed)

    # Slowly run the pump in reverse for the given duration to bubble the reservoir
    def bubble(self, pump_name, duration):
        self.set_speed(pump_name, 0.6)
        self.backward(pump_name)
        self.event_scheduler.schedule(duration, self.stop, pump_name)
        self.event_scheduler.schedule(duration, self.set_speed, pump_name, 1.0)

    # Run the pump forward for 3 seconds then backwards
    def test(self, pump_name):
        self.set_speed(pump_name, 1.0)
        self.forward(pump_name)
        self.event_scheduler.schedule(3, self.backward, pump_name)
        self.event_scheduler.schedule(6, self.stop, pump_name)

    # Prime, wait 2 seconds, then unprime
    def test_prime(self):
        done_time = self.prime('forward')
        self.prime('backward', done_time + 2)

    # Execute any events due
    def update(self):
        self.event_scheduler.execute_due()
