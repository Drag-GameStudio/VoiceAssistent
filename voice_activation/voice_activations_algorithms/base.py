from abc import abstractmethod, ABC

class BaseVAAlgorithm(ABC):
    @abstractmethod
    def predict(self, audio_frame) -> bool:
        ...
