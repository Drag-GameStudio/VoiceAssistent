from .base import BaseVActingAlgorithm
from .edge_algorithm import GoogleVActingAlgorithm
import threading
import os
import time
from elevenlabs.client import ElevenLabs


class ApiSideVActingAlgorithm(GoogleVActingAlgorithm):
    OUTPUT_FOLDER_PATH = ".temp_folder"

    def __init__(self, *args, api_key: str):
        super().__init__(*args)
        self.client = ElevenLabs(
            api_key="e074085169d0366df5b48f5dba1e467adf8fc0c8b6bf1d8738e89486ea1afb07"
        )
        # available_voices = self.client.voices.get_all().voices
        # print(available_voices)


    def gen_sound(self, id, request):
        file_path = self.get_voice_path(id)
        time.sleep(id)
        try:
            audio = self.client.text_to_speech.convert(
                text=request,
                voice_id="hpp4J3VqNfWAUOO0d1Us",
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            with open(file_path, "wb") as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            print(f"Ошибка gTTS: {e}")
            return        

    

        