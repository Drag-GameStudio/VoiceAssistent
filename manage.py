import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "data_base.settings")
django.setup()

from voice_activation.voice_activations_algorithms.outsider import PVAlgorithm
from voice_activation.voice_activations_algorithms.text import VAText
from voice_activation.va_manage import VAManager

from voice_listen.voice_listen_manage import VLManager
from voice_listen.voice_listen_algorithms.outsider import CloudVLA, VoskVLA
from voice_listen.voice_listen_algorithms.text import VLAText

from engine.engine_manage import EngineManager
from engine.engines.llm_engine import GroqLLMEngine, History

from voice_acting.voice_acting_manage import VActingManager
from voice_acting.voice_acting_algorithms.edge_algorithm import EdgeVActingAlgorithm, GoogleVActingAlgorithm
from voice_acting.voice_acting_algorithms.text import VActingText

from engine.engines.promts import general_prompt_create, DONATIK_ID
from singleton_models.middleware import middleware_object
from process_control.runner import create_handler

from dotenv import load_dotenv
load_dotenv()



class Manager:
    def __init__(self, va_manager: VAManager, vl_manager: VLManager):
        self.va_manager = va_manager
        self.vl_manager = vl_manager

    def start(self):
        while True:
            self.va_manager.listen_micro(multi_worker=False)
            self.vl_manager.listen_micro()


import threading
import subprocess


def start_keep_alive():
    return subprocess.Popen(
        ["speaker-test", "-t", "sine", "-f", "1", "-l", "0"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

if __name__ == "__main__":
    groq_api_key = os.getenv("GROQ_API_KEY")
    word_api_key = os.getenv("WORD_API_KEY")

    threading.Thread(target=start_keep_alive).start()

    bot_settings = general_prompt_create("ru", DONATIK_ID)
    engine = GroqLLMEngine(api_key=groq_api_key, history=History(bot_settings))
    e_manager = EngineManager(engine)

    predict_algorithm = PVAlgorithm(word_api_key, "alexa")
    # predict_algorithm = VAText()
    va_manager = VAManager(predict_algorithm)

    edge_alg = GoogleVActingAlgorithm()
    # edge_alg = VActingText()
    vacting_manager = VActingManager(edge_alg)
    

    vla = CloudVLA(create_handler(va_manager, vacting_manager, e_manager))
    vl_manager = VLManager(vla)

    manager = Manager(va_manager, vl_manager)    
    manager.start()    
        
