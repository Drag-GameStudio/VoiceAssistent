import sys
from .base import BaseVActingAlgorithm
import asyncio
import edge_tts
import os
import pygame
from mutagen.mp3 import MP3
import time
from gtts import gTTS
from pathos.helpers import mp as multiprocessing
from sounds.sound_control import PlayAudioManager
from singleton_models.middleware import middleware_object
from process_control.runner import kill_thread


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
            middleware_object.start_action("on_error")

        finally:
            print("Завершаю цикл...")
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

        if os.path.exists(self.OUTPUT_FILE_PATH) and os.path.getsize(self.OUTPUT_FILE_PATH) > 0:
            PlayAudioManager().play_sound(self.OUTPUT_FILE_PATH).join()

            if os.path.exists(self.OUTPUT_FILE_PATH):
                os.remove(self.OUTPUT_FILE_PATH)


import threading
class GoogleVActingAlgorithm(BaseVActingAlgorithm):
    OUTPUT_FOLDER_PATH = ".temp_folder"

    def __init__(self, *args, lang: str = "ru"):
        super().__init__(*args)
        self.lang = lang


    def get_voice_path(self, id):
        return os.path.join(self.OUTPUT_FOLDER_PATH, f"voice_{id}.mp3")

    def gen_sound(self, id, request):
        
        file_path = self.get_voice_path(id)
        time.sleep(id)
        try:
            tts = gTTS(text=request, lang=self.lang, slow=False)
            tts.save(file_path)
        except Exception as e:
            print(f"Ошибка gTTS: {e}")
            return        

    def play_sound_by_id(self, id):
        file_path = self.get_voice_path(id)
        if os.path.exists(file_path):
            PlayAudioManager().play_sound(file_path, is_thread=False)
            os.remove(file_path)
            return True
        return False

    def acting(self, request: str):
        req_parts = request.split(".")
        if len(req_parts[-1]) < 2:
            req_parts.pop(len(req_parts) - 1)
        gen_voice_workers = [threading.Thread(target=self.gen_sound, args=(i, part)) for i, part in enumerate(req_parts)]
        for worker in gen_voice_workers:
            worker.start()

        for i, worker in enumerate(gen_voice_workers):
            worker.join()
            self.play_sound_by_id(i)

        