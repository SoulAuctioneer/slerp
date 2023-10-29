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


    # Execute any events due
    def update(self):
        self.event_scheduler.execute_due()

    # Dispense a drink with the given amounts of Cyan / Magenta / Yellow / Extra, from 0 to 10 
    def dispense(self, cyan, magenta, yellow, extra):

        print('Dispensing drink')

        # Initialize the pump pins
        self.pump_cyan = Motor(PUMP_CYAN_OUT, PUMP_CYAN_IN)
        self.pump_magenta = Motor(PUMP_MAGENTA_OUT, PUMP_MAGENTA_IN)
        self.pump_yellow = Motor(PUMP_YELLOW_OUT, PUMP_YELLOW_IN)
        self.pump_extra = Motor(PUMP_EXTRA_OUT, PUMP_EXTRA_IN)

        # Prime all liquids to the top of the collector
        self.pump_cyan.forward
        self.pump_magenta.forward
        self.pump_yellow.forward
        self.pump_extra.forward
        self.event_scheduler.schedule(DISPENSER_PRIME_DURATION, self.pump_cyan.stop)
        self.event_scheduler.schedule(DISPENSER_PRIME_DURATION, self.pump_magenta.stop)
        self.event_scheduler.schedule(DISPENSER_PRIME_DURATION, self.pump_yellow.stop)
        self.event_scheduler.schedule(DISPENSER_PRIME_DURATION, self.pump_extra.stop)

        # Iterate up to max times, scheduling liquid to pump if more of its color is still needed
        timer = 0
        for i in range(DISPENSER_MAX_SQUIRTS):
            if cyan > i:
                self.event_scheduler.schedule(timer, self.pump_cyan.forward)
                timer += DISPENSER_SQUIRT_DURATION
                self.event_scheduler.schedule(timer, self.pump_cyan.stop)
                timer += DISPENSER_SQUIRT_REST_DURATION
            if magenta > i:
                self.event_scheduler.schedule(timer, self.pump_magenta.forward)
                timer += DISPENSER_SQUIRT_DURATION
                self.event_scheduler.schedule(timer, self.pump_magenta.stop)
                timer += DISPENSER_SQUIRT_REST_DURATION
            if yellow > i:
                self.event_scheduler.schedule(timer, self.pump_yellow.forward)
                timer += DISPENSER_SQUIRT_DURATION
                self.event_scheduler.schedule(timer, self.pump_yellow.stop)
                timer += DISPENSER_SQUIRT_REST_DURATION
            if extra > i:
                self.event_scheduler.schedule(timer, self.pump_extra.forward)
                timer += DISPENSER_SQUIRT_DURATION
                self.event_scheduler.schedule(timer, self.pump_extra.stop)
                timer += DISPENSER_SQUIRT_REST_DURATION

        # Suck all the liquids back into the reservoir
        timer += DISPENSER_SUCK_WAIT_DURATION
        self.event_scheduler.schedule(timer, self.pump_cyan.backward)
        self.event_scheduler.schedule(timer, self.pump_magenta.backward)
        self.event_scheduler.schedule(timer, self.pump_yellow.backward)
        self.event_scheduler.schedule(timer, self.pump_extra.backward)

        # Stop sucking
        timer += DISPENSER_SUCK_DURATION
        self.event_scheduler.schedule(timer, self.pump_cyan.stop)
        self.event_scheduler.schedule(timer, self.pump_magenta.stop)
        self.event_scheduler.schedule(timer, self.pump_yellow.stop)
        self.event_scheduler.schedule(timer, self.pump_extra.stop)

