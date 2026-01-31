from.engines.base import BaseEngine


class EngineManager:
    def __init__(self, engine: BaseEngine):
        self.engine = engine

    def handle(self, request):
        response = self.engine.handle(request)
        return response

