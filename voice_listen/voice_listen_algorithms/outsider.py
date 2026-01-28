import pyaudio
import vosk
import json
from .base import VLABase


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
                self.send_request(result['text'])

        self.stream.stop_stream()
        self.stream.close()
        
