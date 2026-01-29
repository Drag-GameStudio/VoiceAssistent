import pyaudio
import numpy as np
from .voice_activations_algorithms.base import BaseVAAlgorithm
from singleton_models.py_audio_singleton import PyAudioManager
import audioop


class VAManager:

    def __init__(self, predict_algorithm: BaseVAAlgorithm):
        self.predict_algorithm = predict_algorithm


    def start_stream(self):
        
        self.stream = PyAudioManager().py_audio.open(format=self.predict_algorithm.FORMAT,
                                                      channels=self.predict_algorithm.CHANNELS, 
                                                      rate=48000, 
                                                      input=True, 
                                                      frames_per_buffer=self.predict_algorithm.CHUNK)


    def listen_micro(self):
        self.start_stream()
        self.state = None
        while True:
            data = self.stream.read(1536, exception_on_overflow=False)
            data_16k, self.state = audioop.ratecv(data, 2, 1, 48000, 16000, self.state)
            activated = self.predict_algorithm.predict(data_16k)
            if activated:
                print("activate")
                break

        self.stream.stop_stream()
        self.stream.close()

