from voice_activation.voice_activations_algorithms.outsider import PVAlgorithm
from voice_activation.va_manage import VAManager
from voice_listen.voice_listen_manage import VLManager
from voice_listen.voice_listen_algorithms.outsider import CloudVLA
from engine.engine_manage import GPTModel

import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
word_api_key = os.getenv("WORD_API_KEY")

class Manager:
    def __init__(self, va_manager: VAManager, vl_manager: VLManager):
        self.va_manager = va_manager
        self.vl_manager = vl_manager

    def start(self):
        while True:
            self.va_manager.listen_micro()
            self.vl_manager.listen_micro()

if __name__ == "__main__":
    predict_algorithm = PVAlgorithm(word_api_key, "alexa")
    
    va_manager = VAManager(predict_algorithm)

    vla = CloudVLA(lambda request: print("lamda", GPTModel(api_key=groq_api_key, use_random=False).get_answer_without_history([{"role": "user", "content": request}])))
    vl_manager = VLManager(vla)


    manager = Manager(va_manager, vl_manager)    
    manager.start()    
        
