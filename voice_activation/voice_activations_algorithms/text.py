from .base import BaseVAAlgorithm

class VAText(BaseVAAlgorithm):
    def predict(self, audio_frame):
        text = input("Enter activate: ")
        return True