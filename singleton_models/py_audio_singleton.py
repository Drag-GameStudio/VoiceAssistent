import pyaudio
import time

class PyAudioManager:
    _instance = None
    stream = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.py_audio = pyaudio.PyAudio()
        return cls._instance
    
    def start_stream(self, *args, **kwargs):
        if self.stream is not None:
            return self.stream
        
        self.stream = self.py_audio.open(*args, **kwargs)
        return self.stream

    def stop_stream(self):
        if self.stream is not None:
            self.stream.stop_stream()
            while self.stream.is_active():
                time.sleep(0.02)
            self.stream.close()
            self.stream = None

    def get_current_stream_info(self):
        if self.stream is None:
            return None

        info = {
            "format": self.stream._format,              
            "channels": self.stream._channels,          
            "rate": int(self.stream._rate),             
            "frames_per_buffer": self.stream._frames_per_buffer,
        }

        return info

    def get_index(self):
        p = self.py_audio
        try:
            device_count = p.get_device_count()
        except Exception:
            return 0 
        
        for i in range(device_count):
            try:
                device_info = p.get_device_info_by_index(i)
                if device_info.get('maxInputChannels') > 0:
                    return i
            except Exception:
                continue
            
        return 0