
from pathos.helpers import mp as multiprocessing
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

class PlayAudioManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_file_path(self, sound_name):
        return sound_name

    def play_sound_process(self, file_path: str):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass

        pygame.mixer.music.unload()
        pygame.mixer.quit()

    def play_sound(self, sound_name: str, with_daemon=False):
        file_path = self.get_file_path(sound_name)
        sound_process = multiprocessing.Process(target=self.play_sound_process, args=(file_path,))

        sound_process.daemon = with_daemon
        sound_process.start()

        return sound_process
