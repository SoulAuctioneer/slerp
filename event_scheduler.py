from pygame import time

class EventScheduler:

    def __init__(self):
        self.scheduled_events = []

    # schedule a function to run once after the given delay 
    def schedule(self, delay, function, *args, **kwargs):
        trigger_time = time.get_ticks() + (delay * 1000)
        self.scheduled_events.append({'function': function, 'trigger_time': trigger_time, 'args': args, 'kwargs': kwargs})

    # Execute any events whose scheduled time has passed
    def execute_due(self):
        current_time = time.get_ticks()
        for event in self.scheduled_events[:]:
            if current_time >= event['trigger_time']:
                event['function'](*event['args'], **event['kwargs'])
                self.scheduled_events.remove(event)
