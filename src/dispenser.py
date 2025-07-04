try:
    from gpiozero import Motor, Device, PWMOutputDevice
    from gpiozero.pins.mock import MockFactory, MockPWMPin
    GPIOZERO_AVAILABLE = True
except ImportError:
    GPIOZERO_AVAILABLE = False
    # Create dummy classes if gpiozero is not available
    class Motor:
        def __init__(self, *args, **kwargs): pass
        def forward(self): pass
        def backward(self): pass
        def stop(self): pass

    class Device:
        pin_factory = None

    class PWMOutputDevice:
        def __init__(self, *args, **kwargs): pass
        value = 0
    
    class MockFactory:
        def __init__(self, *args, **kwargs): pass

    class MockPWMPin:
        def __init__(self, *args, **kwargs): pass

from .service_locator import ServiceLocator
import platform
from .settings import *

class Dispenser:
    def __init__(self):
        self._event_manager = ServiceLocator.get("event_manager")
        self._event_scheduler = ServiceLocator.get("event_scheduler")
        self._event_manager.subscribe("DISPENSE_DRINK", self.dispense)
        self._event_manager.subscribe("TEST_PUMP", self.test)
        self._event_manager.subscribe("TEST_PRIME", self.test_prime)
        self._event_manager.subscribe("SCHEDULE_BUBBLE", self.schedule_bubble_event)

        if not GPIOZERO_AVAILABLE or (platform.system() != 'Linux' or platform.machine() != 'aarch64'):
            print('gpiozero is not available or not on a Raspberry Pi, using mock objects')
            Device.pin_factory = MockFactory(pin_class=MockPWMPin)

        self.pumps = {
            'cyan': {'motor': Motor(PUMP_CYAN_OUT, PUMP_CYAN_IN), 'prime_duration': PUMP_CYAN_PRIME_DURATION, 'speed': PWMOutputDevice(PUMP_CYAN_SPEED)},
            'magenta': {'motor': Motor(PUMP_MAGENTA_OUT, PUMP_MAGENTA_IN), 'prime_duration': PUMP_MAGENTA_PRIME_DURATION, 'speed': PWMOutputDevice(PUMP_MAGENTA_SPEED)},
            'yellow': {'motor': Motor(PUMP_YELLOW_OUT, PUMP_YELLOW_IN), 'prime_duration': PUMP_YELLOW_PRIME_DURATION, 'speed': PWMOutputDevice(PUMP_YELLOW_SPEED)},
            'transparent': {'motor': Motor(PUMP_TRANSPARENT_OUT, PUMP_TRANSPARENT_IN), 'prime_duration': PUMP_TRANSPARENT_PRIME_DURATION, 'speed': PWMOutputDevice(PUMP_TRANSPARENT_SPEED)}
        }
        for pump_name in self.pumps.keys():
            self.set_speed(pump_name, 1.0)

    def dispense(self, drink, on_complete=None, *args, **kwargs):
        timer = self.prime('forward') + 0.1
        for i in range(max(drink.cmyt)):
            for pump_name, amount in {'cyan': drink.cmyt[0], 'magenta': drink.cmyt[1], 'yellow': drink.cmyt[2], 'transparent': drink.cmyt[3]}.items():
                if amount > i:
                    self.schedule_forward(timer, pump_name)
                    # self.event_scheduler.schedule(timer, self.set_led, drink.rgb)
                    timer += DISPENSER_SQUIRT_DURATION
                    self.schedule_stop(timer, pump_name)
                    # self.event_scheduler.schedule(timer, self.reset_led)
                    timer += DISPENSER_SQUIRT_REST_DURATION
        timer += DISPENSER_SUCK_WAIT_DURATION
        timer += self.prime('backward', timer)
        if on_complete:
            self._event_scheduler.schedule(timer, on_complete, *args, **kwargs)
        return timer
    
    def prime(self, direction, start_timer=0, speed=1.0):
        if not self.pumps:
            return 0
        max_prime_duration = max(pump['prime_duration'] for pump in self.pumps.values())
        for pump_name, pump in self.pumps.items():
            pump_start_timer = start_timer + max_prime_duration - pump['prime_duration']
            self.schedule_set_speed(pump_start_timer, pump_name, speed)
            if direction == 'forward':
                self.schedule_forward(pump_start_timer, pump_name)
            else:
                self.schedule_backward(pump_start_timer, pump_name)
            self.schedule_stop(start_timer + max_prime_duration, pump_name)
        return max_prime_duration

    def forward(self, pump_name): self.pumps[pump_name]['motor'].forward()
    def schedule_forward(self, start_timer, pump_name): self._event_scheduler.schedule(start_timer, self.forward, pump_name)
    def backward(self, pump_name): self.pumps[pump_name]['motor'].backward()
    def schedule_backward(self, start_timer, pump_name): self._event_scheduler.schedule(start_timer, self.backward, pump_name)
    def stop(self, pump_name): self.pumps[pump_name]['motor'].stop()
    def schedule_stop(self, start_timer, pump_name): self._event_scheduler.schedule(start_timer, self.stop, pump_name)
    def set_speed(self, pump_name, speed): self.pumps[pump_name]['speed'].value = speed
    def schedule_set_speed(self, start_timer, pump_name, speed): self._event_scheduler.schedule(start_timer, self.set_speed, pump_name, speed)

    def bubble(self, pump_name, duration=3):
        self.set_speed(pump_name, 0.4)
        self.backward(pump_name)
        self._event_scheduler.schedule(duration, self.stop, pump_name)
        self._event_scheduler.schedule(duration, self.set_speed, pump_name, 1.0)

    def schedule_bubble_event(self, start_timer, pump_name, duration):
        self._event_scheduler.schedule(start_timer, self.bubble, pump_name, duration)

    def test(self, pump_name):
        self.set_speed(pump_name, 1.0)
        self.forward(pump_name)
        prime_duration = self.pumps[pump_name]['prime_duration']
        self._event_scheduler.schedule(prime_duration, self.backward, pump_name)
        self._event_scheduler.schedule(prime_duration * 2, self.stop, pump_name)

    def test_prime(self):
        done_time = self.prime('forward')
        done_time += self.prime('backward', done_time + 1)
        done_time += self.prime('backward', done_time + 1, speed=0.4)
