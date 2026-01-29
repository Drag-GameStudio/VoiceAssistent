from .base import BaseVActingAlgorithm
import asyncio
import edge_tts
import os
import pygame
from voice_activation.va_manage import VAManager
from mutagen.mp3 import MP3
import time
from multiprocessing import Process


import sys
import signal

def test(stop_at, OUTPUT_FILE_PATH):

    def cleanup(signum, frame):
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        sys.exit(0)
    
    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE_PATH)

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)


    try:
        pygame.mixer.music.play()
        start_time = time.time()
        
        while pygame.mixer.music.get_busy():
            if time.time() - start_time >= stop_at:
                pygame.mixer.music.stop()
                break
            time.sleep(0.02)

    except:
        pass

class EdgeVActingAlgorithm(BaseVActingAlgorithm):
    OUTPUT_FILE_PATH = "voice.mp3"

    def __init__(self, *args, voice: str = "ru-RU-SvetlanaNeural", va_manager: VAManager):
        super().__init__(*args)
        self.voice = voice
        self.va_manager = va_manager



    def acting(self, request):

        

        communicate = edge_tts.Communicate(request, self.voice)
        asyncio.run(communicate.save(self.OUTPUT_FILE_PATH))

        audio = MP3(self.OUTPUT_FILE_PATH)
        duration = audio.info.length
        stop_at = max(0, duration - 0.5) 

        acting_run = Process(target=test, args=(stop_at, self.OUTPUT_FILE_PATH))

        acting_run.start()
        self.va_manager.listen_micro()
        acting_run.terminate()
        acting_run.join()

        

        if os.path.exists(self.OUTPUT_FILE_PATH):
            os.remove(self.OUTPUT_FILE_PATH)



        

        

