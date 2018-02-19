
class BaseStrategy:

    def __init__(self, name, description, sources, params, duration, config_key):
        self.name = name
        self.description = description
        self.sources = sources
        self.params = params
        self.duration = duration
        self.config_key = config_key

    def run(self):
        pass

    def set_config(self, config):
        pass
