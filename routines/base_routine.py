class BaseRoutine:
    def __init__(self, app):
        self.app = app

    def load(self):
        """Load any assets or perform setup for the routine."""
        raise NotImplementedError

    def get_start_scene(self):
        """Return the starting scene class for this routine."""
        raise NotImplementedError

    def get_drinks_scene(self):
        """Return the drinks selection scene class for this routine."""
        raise NotImplementedError

    def get_drinks(self):
        """Return the dictionary of available drinks."""
        raise NotImplementedError 