import ctypes
import threading
from voice_activation.voice_activations_algorithms.outsider import PVAlgorithm
from voice_activation.va_manage import VAManager
from voice_listen.voice_listen_manage import VLManager
from voice_listen.voice_listen_algorithms.outsider import CloudVLA, VoskVLA
from engine.engine_manage import EngineManager
from engine.engines.llm_engine import GroqLLMEngine
from voice_acting.voice_acting_manage import VActingManager
from voice_acting.voice_acting_algorithms.edge_algorithm import EdgeVActingAlgorithm, GoogleVActingAlgorithm 
from process_control.runner import run_multi_va_and_task
from singleton_models.middleware import middleware_object
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
            self.va_manager.listen_micro(multi_worker=False)
            self.vl_manager.listen_micro()

def create_handler(va_manager, vacting_manager: VActingManager, e_manager: EngineManager):
    def handle_request(request: str):
        print(request)
        return run_multi_va_and_task(request, va_manager, lambda request: vacting_manager.acting(e_manager.handle(request)))
    
    return handle_request

if __name__ == "__main__":

    edge_alg = GoogleVActingAlgorithm()
    vacting_manager = VActingManager(edge_alg)

    engine = GroqLLMEngine(api_key=groq_api_key)
    e_manager = EngineManager(engine)

    predict_algorithm = PVAlgorithm(word_api_key, "alexa")
    va_manager = VAManager(predict_algorithm)

    vla = VoskVLA(create_handler(va_manager, vacting_manager, e_manager))
    vl_manager = VLManager(vla)

    manager = Manager(va_manager, vl_manager)    
    manager.start()    
        
