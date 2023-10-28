from gpiozero import Motor
import event_scheduler
import platform

class Dispenser:
    def __init__(self):
        # Only enable on raspberry pi
        self.enabled = platform.system() == 'Linux' and platform.machine() == 'armv7l'
        self.pump_cyan = None
        self.pump_magenta = None
        self.arduino = None
        self.motor_pin = 18
        self.event_scheduler = event_scheduler.EventScheduler()

        if self.enabled:
            print('Initializing GPIO communication')
            self.pump_cyan = Motor(24, 23)
            self.pump_magenta = Motor(22, 27)
        else:
            print('gpiozero is disabled')

    def update(self):
        self.event_scheduler.execute_due()

    def dispense(self, drink):
        print('Dispensing drink')
        if not self.enabled:
            return
        self.event_scheduler.schedule(0, self.pump_cyan.forward)
        self.event_scheduler.schedule(0, self.pump_magenta.forward)
        self.event_scheduler.schedule(4, self.pump_cyan.stop)
        self.event_scheduler.schedule(4, self.pump_magenta.stop)
        for i in range(10):
            self.event_scheduler.schedule(4 + i * 0.38, self.pump_cyan.forward)
            self.event_scheduler.schedule(4 + i * 0.38 + 0.33, self.pump_cyan.stop)
            self.event_scheduler.schedule(4 + i * 0.38 + 0.38, self.pump_magenta.forward)
            self.event_scheduler.schedule(4 + i * 0.38 + 0.38 + 0.33, self.pump_magenta.stop)
        self.event_scheduler.schedule(12, self.pump_cyan.backward)
        self.event_scheduler.schedule(12, self.pump_magenta.backward)
        self.event_scheduler.schedule(17, self.pump_cyan.stop)
        self.event_scheduler.schedule(17, self.pump_magenta.stop)

