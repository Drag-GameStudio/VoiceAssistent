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