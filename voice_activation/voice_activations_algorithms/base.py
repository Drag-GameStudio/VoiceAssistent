from abc import abstractmethod, ABC
import pyaudio
from process_control.init_control import MultiProccessActivation

class BaseVAAlgorithm(ABC, MultiProccessActivation):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1280

    def predict(self, audio_frame) -> bool:
        self.init_preccessing()
