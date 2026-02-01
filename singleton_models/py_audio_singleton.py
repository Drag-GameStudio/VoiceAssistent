import pyaudio


class PyAudioManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.py_audio = pyaudio.PyAudio()
        return cls._instance
    
    def get_index(self):
        p = self.py_audio
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        
        for i in range(0, num_devices):
            device_info = p.get_device_info_by_index(i)
            # Проверяем, что у устройства есть входные каналы (это микрофон)
            if device_info.get('maxInputChannels') > 0:
                print(f"Найдено подходящее устройство: {device_info.get('name')} (Индекс: {i})")
                p.terminate()
                return i
                
        p.terminate()
        return None