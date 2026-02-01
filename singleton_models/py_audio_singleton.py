import pyaudio


class PyAudioManager:
    _instance = None
    stream = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.py_audio = pyaudio.PyAudio()
        return cls._instance
    
    def start_stream(self, *args, **kwargs):
        self.stream = self.py_audio.open(*args, **kwargs)
        return self.stream

    def stop_stream(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

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