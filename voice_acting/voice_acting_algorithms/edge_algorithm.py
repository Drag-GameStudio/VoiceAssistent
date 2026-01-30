import sys
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
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        communicate = edge_tts.Communicate(request, self.voice)

        loop = asyncio.new_event_loop()
    
        try:
            loop.run_until_complete(communicate.save(self.OUTPUT_FILE_PATH))
        except Exception as e:
            print(f"Сетевая ошибка (игнорируем): {e}")
        finally:
            print("Завершаю цикл...")
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

        if os.path.exists(self.OUTPUT_FILE_PATH) and os.path.getsize(self.OUTPUT_FILE_PATH) > 0:
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

import os
import pygame
from gtts import gTTS

class GoogleVActingAlgorithm(BaseVActingAlgorithm):
    OUTPUT_FILE_PATH = "voice.mp3"

    def __init__(self, *args, lang: str = "ru"):
        super().__init__(*args)
        self.lang = lang

    def acting(self, request: str):
        try:
            # Создаем объект TTS (использует API переводчика)
            tts = gTTS(text=request, lang=self.lang, slow=False)
            tts.save(self.OUTPUT_FILE_PATH)
        except Exception as e:
            print(f"Ошибка gTTS: {e}")
            return

        # Блок воспроизведения (ваш стандартный pygame)
        if os.path.exists(self.OUTPUT_FILE_PATH):
            pygame.mixer.init()
            pygame.mixer.music.load(self.OUTPUT_FILE_PATH)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.unload()
            pygame.mixer.quit()
            os.remove(self.OUTPUT_FILE_PATH)