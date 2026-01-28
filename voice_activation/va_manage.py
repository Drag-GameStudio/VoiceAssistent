import pyaudio
import numpy as np
from .voice_activations_algorithms.base import BaseVAAlgorithm
from .voice_activations_algorithms.outsider import OWKAlgorithm
from singleton_models.py_audio_singleton import PyAudioManager



class VAManager:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1280 


    def __init__(self, predict_algorithm: BaseVAAlgorithm):
        self.predict_algorithm = predict_algorithm

    def start_stream(self):
        self.stream = PyAudioManager().py_audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)


    def listen_micro(self):
        self.start_stream()
        while True:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            audio_frame = np.frombuffer(data, dtype=np.int16)

            activated = self.predict_algorithm.predict(audio_frame)
            if activated:
                print("activate")
                break

        self.stream.stop_stream()
        self.stream.close()


if __name__ == "__main__":
    predict_algorithm = OWKAlgorithm("alexa")
    va_manager = VAManager(predict_algorithm)
    va_manager.listen_micro()