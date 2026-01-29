from voice_activation.voice_activations_algorithms.outsider import PVAlgorithm
from voice_activation.va_manage import VAManager
from voice_listen.voice_listen_manage import VLManager
from voice_listen.voice_listen_algorithms.outsider import VoskVLA, SRVLA, CloudVLA


    

class Manager:
    def __init__(self, va_manager: VAManager, vl_manager: VLManager):
        self.va_manager = va_manager
        self.vl_manager = vl_manager

    def start(self):
        while True:
            self.va_manager.listen_micro()
            self.vl_manager.listen_micro()

if __name__ == "__main__":
    predict_algorithm = PVAlgorithm("alexa")
    
    va_manager = VAManager(predict_algorithm)

    vla = CloudVLA(lambda request: print("lamda", request))
    vl_manager = VLManager(vla)


    manager = Manager(va_manager, vl_manager)    
    manager.start()    
        
