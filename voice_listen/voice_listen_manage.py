from .voice_listen_algorithms.base import VLABase
from .voice_listen_algorithms.outsider import VoskVLA
from singleton_models.py_audio_singleton import PyAudioManager
from singleton_models.middleware import middleware_object

class VLManager:
    def __init__(self, vla: VLABase):
        self.vla = vla

    def listen_micro(self):
        self.vla.configurate(PyAudioManager().py_audio)
        self.vla.listen_micro()
        middleware_object.start_action("stop_listening")


if __name__ == "__main__":
    ...
    # vla = VoskVLA(lambda request: print("lamda", request))
    # vl_manager = VLManager(vla)

    # vl_manager.listen_micro()