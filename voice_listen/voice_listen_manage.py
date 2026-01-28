from .voice_listen_algorithms.base import VLABase
from .voice_listen_algorithms.outsider import VoskVLA
from singleton_models.py_audio_singleton import PyAudioManager


class VLManager:
    def __init__(self, vla: VLABase):
        self.vla = vla

    def listen_micro(self):
        self.vla.configurate(PyAudioManager().py_audio)
        self.vla.listen_micro()


if __name__ == "__main__":
    ...
    # vla = VoskVLA(lambda request: print("lamda", request))
    # vl_manager = VLManager(vla)

    # vl_manager.listen_micro()