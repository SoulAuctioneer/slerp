from src.service_locator import ServiceLocator

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.screen = None
        self._event_manager = ServiceLocator.get("event_manager")
        self._event_manager.subscribe('CHANGE_SCENE', self.set_scene)

    def set_scene(self, scene_class=None, **kwargs):
        if scene_class:
            self.current_scene = scene_class(screen=self.screen, **kwargs)
            if self.current_scene:
                self.current_scene.run()
        else:
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