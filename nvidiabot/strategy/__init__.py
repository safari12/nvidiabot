
class BaseStrategy:

    def __init__(self, name, description, sources, params, duration):
        self.name = name
        self.description = description
        self.sources = sources
        self.params = params
        self.duration = duration

    def run(self):
        pass
