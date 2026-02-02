import pyaudio
import vosk
import json
from .base import VLABase
import os
from singleton_models.middleware import middleware_object
from singleton_models.py_audio_singleton import PyAudioManager



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
import struct
import math

class CloudVLA(VLABase):
    def __init__(self, *args, lang="ru", timeout: float = 5):
        super().__init__(*args)
        self.recognizer = sr.Recognizer()
        self.lang = "ru-RU" if lang == "ru" else "en-US"
        self.timeout = timeout
        self.source = None
        self.mic_index = PyAudioManager().get_index()
        
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
                PyAudioManager().stop_stream()
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


                    
            except Exception as e:
                print(e)
                middleware_object.start_action("on_error")
            finally:
                if os.path.exists(wave_path):
                    try:
                        os.remove(wave_path)
                    except PermissionError:
                        print("Не удалось удалить временный файл, он еще занят.")


class CloudVLAPyAudio(VLABase):
    def __init__(self, *args, lang="ru", timeout: float = 5):
        super().__init__(*args)
        self.recognizer = sr.Recognizer()
        self.lang = "ru-RU" if lang == "ru" else "en-US"
        self.timeout = timeout
        self.source = None
        self.mic_index = PyAudioManager().get_index()
        self.pam = PyAudioManager()
        
        print("READY")

    def get_rms(self, data):
        
        count = len(data) / 2
        if count == 0:
            return 0
        format = "%dh" % (count)
        shorts = struct.unpack(format, data)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * (1.0 / 32768)
            sum_squares += n * n
        return math.sqrt(sum_squares / count)

    def recognize_text(self):

        THRESHOLD = 0.01
        SILENCE_LIMIT = 2


        stream_info = self.pam.get_current_stream_info()
        if stream_info is None:
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000

            stream = self.pam.start_stream(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        else:
            CHUNK = stream_info["frames_per_buffer"]
            RATE = stream_info["rate"]
            stream = self.pam.start_stream()

        audio2send = []
        rel = RATE / CHUNK
        slid_win = []
        prev_audio = []
        started = False
        
        silence_start = None 

        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            slid_win.append(math.sqrt(abs(self.get_rms(data))))
            
            rms_val = self.get_rms(data)

            if started:
                audio2send.append(data)
                
                if rms_val < THRESHOLD:
                    if silence_start is None:
                        silence_start = time.time()
                    else:
                        if time.time() - silence_start > SILENCE_LIMIT:
                            print("Фраза закончена.")
                            break
                else:
                    silence_start = None
            
            elif rms_val > THRESHOLD:
                print("Обнаружен голос, запись пошла...")
                started = True
                audio2send.extend(prev_audio)
                audio2send.append(data)
                silence_start = None  # Сброс таймера

            prev_audio.append(data)
            if len(prev_audio) > int(rel * 0.5):
                prev_audio.pop(0)
        
        raw_data = b''.join(audio2send)
    
        recognizer = sr.Recognizer()
        audio_source = sr.AudioData(raw_data, RATE, 2)
        
        out = {}
        
        try:
            # Распознаем
            text = recognizer.recognize_google(audio_source, language="ru-RU")
            out = {
                "success": True,
                "text": text,
                "duration": len(raw_data) / RATE / 2
            }
        except sr.UnknownValueError:
            out = {
                "success": False,
                "text": None,
                "error": "Не удалось распознать речь"
            }
        except Exception as e:
            out = {
                "success": False,
                "text": None,
                "error": str(e)
            }
            
        return out

    def listen_micro(self):
        

        while True:
            result = self.recognize_text()
            if result["success"] == False or result["text"] is None or result["text"] == "":
                break
            
            self.send_request(result["text"])
            