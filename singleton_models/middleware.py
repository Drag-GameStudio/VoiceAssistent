from sounds.sound_control import PlayAudioManager

class Middleware:
    _instance = None
    actions: dict[str, list] = {}
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.play_sound_manager = PlayAudioManager()
        return cls._instance

    def activate_by_word(self):
        self.play_sound_manager.play_sound(r"C:\Users\sinic\OneDrive\Документы\GitHub\VoiceAssistent\sounds\source\activating-alarm-buttons-pressed-bleeps-108309.mp3")
    def start_action(self, action_name):
        try:
            use_func = getattr(self, action_name)
            use_func()
        except:
            ...

middleware_object = Middleware()