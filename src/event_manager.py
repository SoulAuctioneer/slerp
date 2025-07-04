class EventManager:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def publish(self, event_type, **kwargs):
        if event_type == "SET_BUTTONS":
            buttons = kwargs.get('buttons', [])
            print(f"DEBUG: Publishing SET_BUTTONS event with {len(buttons)} buttons")
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                if event_type == "SET_BUTTONS":
                    print(f"DEBUG: Calling SET_BUTTONS listener: {listener}")
                listener(**kwargs) 