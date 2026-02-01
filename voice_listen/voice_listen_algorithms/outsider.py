import pyaudio
import vosk
import json
from .base import VLABase
import os
from singleton_models.middleware import middleware_object


class VoskVLA(VLABase):
    def __init__(self, *args, lang="ru"):
        super().__init__(*args)
        self.model = vosk.Model(lang=lang)
        self.rec = vosk.KaldiRecognizer(self.model, 16000)


    def configurate(self, p):
        self.stream = p.open(
            format=pyaudio.paInt16, 
            channels=1, 
            rate=16000, 
            input=True, 
            frames_per_buffer=8000
        )

    def listen_micro(self):
        count_of_empty = 0
        while count_of_empty < 2:
            data = self.stream.read(4000, exception_on_overflow=False)
            
            if len(data) == 0:
                break

            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                if result['text'] == "":
                    count_of_empty += 1
                self.end_listen()
                self.send_request(result['text'])

        self.stream.stop_stream()
        self.stream.close()
        

import speech_recognition as sr
import os
import tempfile
import time

class CloudVLA(VLABase):
    def __init__(self, *args, lang="ru", timeout: float = 5):
        super().__init__(*args)
        self.recognizer = sr.Recognizer()
        self.lang = "ru-RU" if lang == "ru" else "en-US"
        self.timeout = timeout
        self.source = None
        self.mic_index = 1 if os.name != 'nt' else None 
        
        print("READY")

    def prep(self):
        if self.source is None:
            self.source = sr.Microphone(device_index=self.mic_index, sample_rate=48000)
        
    def listen_micro(self):
        tmp_dir = tempfile.gettempdir()
        wave_path = os.path.join(tmp_dir, "voice_temp.wav")

        
        self.recognizer.pause_threshold = 2
        self.recognizer.non_speaking_duration = 1.0
        self.recognizer.energy_threshold = 130
        self.recognizer.operation_timeout = self.timeout
        self.prep()

        while True:
            try:
                with self.source as source:
                    audio_data = self.recognizer.listen(source, timeout=self.timeout, phrase_time_limit=None)
            except sr.WaitTimeoutError:
                print("Вы молчали слишком долго (5 секунд). Выключаю микрофон.")
                break

            self.end_listen()

            with open(wave_path, "wb") as f:
                f.write(audio_data.get_wav_data())

            print("Обработка...")
            
            try:
                with sr.AudioFile(wave_path) as source_file:
                    audio_to_send = self.recognizer.record(source_file)
                    text = self.recognizer.recognize_google(audio_to_send, language=self.lang)
                
                if text:
                    time.sleep(0.2)
                    self.send_request(text)
                    time.sleep(0.5)


                    
            except Exception as e:
                print(e)
                middleware_object.start_action("on_error")
            finally:
                if os.path.exists(wave_path):
                    try:
                        os.remove(wave_path)
                    except PermissionError:
                        print("Не удалось удалить временный файл, он еще занят.")