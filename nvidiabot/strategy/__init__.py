
class BaseStrategy:

    def __init__(self, name, description, sources, params, duration, config_key):
        self.name = name
        self.description = description
        self.sources = sources
        self.params = params
        self.duration = duration
        self.config_key = config_key

        self._config = None

    def run(self):
        pass

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value
