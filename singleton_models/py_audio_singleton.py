import pyaudio


class PyAudioManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.py_audio = pyaudio.PyAudio()
        return cls._instance