class BaseRoutine:
    def __init__(self, app):
        self.app = app
        self._state = {}  # For storing routine-specific state
        self._config = {}  # For storing routine-specific configuration

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
    
    def set_state(self, key, value):
        """Set a state value for this routine."""
        self._state[key] = value
    
    def get_state(self, key, default=None):
        """Get a state value for this routine."""
        return self._state.get(key, default)
    
    def set_config(self, config_dict):
        """Set the configuration dictionary for this routine."""
        self._config = config_dict
    
    def get_config(self, key, default=None):
        """Get a configuration value for this routine."""
        return self._config.get(key, default) 