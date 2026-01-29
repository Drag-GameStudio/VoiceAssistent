from .voice_acting_algorithms.base import BaseVActingAlgorithm


class VActingManager:
    def __init__(self, vacting_algorithm: BaseVActingAlgorithm):
        self.vacting_algorithm = vacting_algorithm

    def acting(self, request):
        self.vacting_algorithm.acting(request)