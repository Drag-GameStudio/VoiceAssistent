from abc import abstractmethod, ABC
import pyaudio

class BaseVAAlgorithm(ABC):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1280

    @abstractmethod
    def predict(self, audio_frame) -> bool:
        ...
