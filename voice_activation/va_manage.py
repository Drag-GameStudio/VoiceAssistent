import pyaudio
import numpy as np
from .voice_activations_algorithms.base import BaseVAAlgorithm
from singleton_models.py_audio_singleton import PyAudioManager
from sounds.sound_control import PlayAudioManager
import audioop
from singleton_models.middleware import middleware_object
import os
import signal
import time
import multiprocessing

class VAManager:

    def __init__(self, predict_algorithm: BaseVAAlgorithm):
        self.predict_algorithm = predict_algorithm

    def listen_micro(self, multi_worker: bool = True):
        print("Listening...")
        stream = PyAudioManager().py_audio.open(format=self.predict_algorithm.FORMAT,
                                                      channels=self.predict_algorithm.CHANNELS, 
                                                      rate=48000, 
                                                      input=True, 
                                                      input_device_index=1,
                                                      frames_per_buffer=self.predict_algorithm.CHUNK)

        self.state = None
        while True:
            data = stream.read(1536, exception_on_overflow=False)
            data_16k, self.state = audioop.ratecv(data, 2, 1, 48000, 16000, self.state)
            activated = self.predict_algorithm.predict(data_16k)
            if activated:
                print("activate")
                middleware_object.start_action("activate_by_word")
                break

        stream.stop_stream()
        stream.close()
        self.predict_algorithm.quite_proccessing()
        print("SECOND")

        time.sleep(0.3)
        if multi_worker:
            print("THIRDF")
            os.kill(os.getpid(), signal.SIGKILL)
