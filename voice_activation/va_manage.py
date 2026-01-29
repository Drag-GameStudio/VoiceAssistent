import pyaudio
import numpy as np
from .voice_activations_algorithms.base import BaseVAAlgorithm
from singleton_models.py_audio_singleton import PyAudioManager



class VAManager:

    def __init__(self, predict_algorithm: BaseVAAlgorithm):
        self.predict_algorithm = predict_algorithm


    def start_stream(self):
        
        self.stream = PyAudioManager().py_audio.open(format=self.predict_algorithm.FORMAT,
                                                      channels=self.predict_algorithm.CHANNELS, 
                                                      rate=self.predict_algorithm.RATE, 
                                                      input=True, 
                                                      frames_per_buffer=self.predict_algorithm.CHUNK)


    def listen_micro(self):
        self.start_stream()
        while True:
            data = self.stream.read(self.predict_algorithm.CHUNK)

            activated = self.predict_algorithm.predict(data)
            if activated:
                print("activate")
                break

        self.stream.stop_stream()
        self.stream.close()

