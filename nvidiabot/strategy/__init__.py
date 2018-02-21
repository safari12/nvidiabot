import abc


class Strategy:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, name, description, sources, params, config_key):
        self.name = name
        self.description = description
        self.sources = sources
        self.params = params
        self.config_key = config_key

        self._config = None

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def set_config(self, config):
        self._config = config
        pass

    @abc.abstractmethod
    def get_config(self):
        return self._config
