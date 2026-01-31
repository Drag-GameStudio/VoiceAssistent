from .base import BaseVActingAlgorithm

class VActingText(BaseVActingAlgorithm):
    def acting(self, request):
        print("ACTING:", request)