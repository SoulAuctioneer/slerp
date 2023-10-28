from pygame import time

class EventScheduler:

    def __init__(self):
        self.scheduledEvents = []

    # schedule a function to run once after the given delay 
    def schedule(self, delay, function):
        triggerTime = time.get_ticks() + (delay * 1000)
        self.scheduledEvents.append({'function': function, 'triggerTime': triggerTime})

    # Execute any events whose scheduled time has passed
    def executeDue(self):
        currentTime = time.get_ticks()
        for event in self.scheduledEvents:
            if currentTime >= event['triggerTime']:
                event['function']()
                self.scheduledEvents.remove(event)

