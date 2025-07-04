from src.service_locator import ServiceLocator

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.screen = None
        self._event_manager = ServiceLocator.get("event_manager")
        self._event_manager.subscribe('CHANGE_SCENE', self.set_scene)
        self._event_scheduler = ServiceLocator.get("event_scheduler")

    def set_scene(self, scene_class=None, **kwargs):
        print(f"DEBUG: set_scene called with scene_class: {scene_class.__name__ if scene_class else 'None'}")
        print("DEBUG: Calling reset_buttons")
        ServiceLocator.get("app").reset_buttons()
        # Cancel all scheduled events to prevent stale events from previous scenes
        print("DEBUG: Cancelling all scheduled events")
        self._event_scheduler.cancel_all()
        if scene_class:
            print(f"DEBUG: Creating new scene: {scene_class.__name__}")
            self.current_scene = scene_class(screen=self.screen, **kwargs)
            if self.current_scene:
                print(f"DEBUG: Running scene: {scene_class.__name__}")
                self.current_scene.run()
        else:
            print("DEBUG: Setting current_scene to None")
            self.current_scene = None

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        self.screen = screen
        if self.current_scene:
            self.current_scene.draw(screen)

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events) 