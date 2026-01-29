from .base import BaseVActingAlgorithm
import asyncio
import edge_tts
import os
import pygame

class EdgeVActingAlgorithm(BaseVActingAlgorithm):
    OUTPUT_FILE_PATH = "voice.mp3"

    def __init__(self, *args, voice: str = "ru-RU-SvetlanaNeural"):
        super().__init__(*args)
        self.voice = voice


    def acting(self, request):
        communicate = edge_tts.Communicate(request, self.voice)
        asyncio.run(communicate.save(self.OUTPUT_FILE_PATH))

        pygame.mixer.init()

        pygame.mixer.music.load(self.OUTPUT_FILE_PATH)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pass
        
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        
        if os.path.exists(self.OUTPUT_FILE_PATH):
            os.remove(self.OUTPUT_FILE_PATH)

from mutagen.mp3 import MP3
import time
class EdgeVActingAlgorithmCutting(EdgeVActingAlgorithm):
    def acting(self, request):
        communicate = edge_tts.Communicate(request, self.voice)
        asyncio.run(communicate.save(self.OUTPUT_FILE_PATH))

        audio = MP3(self.OUTPUT_FILE_PATH)
        duration = audio.info.length
        stop_at = max(0, duration - 0.5) 

        pygame.mixer.init()
        pygame.mixer.music.load(self.OUTPUT_FILE_PATH)
        pygame.mixer.music.play()
        
        start_time = time.time()
        
        while pygame.mixer.music.get_busy():
            if time.time() - start_time >= stop_at:
                pygame.mixer.music.stop()
                break
            time.sleep(0.02)
        
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        
        if os.path.exists(self.OUTPUT_FILE_PATH):
            os.remove(self.OUTPUT_FILE_PATH)