
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import threading
import subprocess

class PlayAudioManager:
    BASE_SS_FOLDER = os.path.abspath("sounds/source")
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_file_path(self, sound_name):
        if sound_name[:2] == "ss":
            return os.path.join(self.BASE_SS_FOLDER, sound_name[2:])
        return sound_name

    def play_sound_process(self, file_path: str):
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(48000, -16, 2, 1024)
            pygame.mixer.init()

        sound = pygame.mixer.Sound(file_path)
        try:
            channel = sound.play()
            while channel.get_busy():
                time.sleep(0.1)
        finally:
            channel.stop()



    def play_sound(self, sound_name: str, is_thread=True, with_daemon=False):
        file_path = self.get_file_path(sound_name)
        if is_thread:
            sound_process = threading.Thread(target=self.play_sound_process, args=(file_path,))
            sound_process.daemon = with_daemon
            sound_process.start()

            return sound_process
        
        self.play_sound_process(file_path)
