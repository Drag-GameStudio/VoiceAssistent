from .base import BaseVAAlgorithm
import pvporcupine
import pyaudio
import struct



# class OWKAlgorithm(BaseVAAlgorithm):

#     def __init__(self, model_name = "alexa" ):
#         super().__init__()
#         self.model_name = model_name
#         self.oww_model = openwakeword.Model(wakeword_models=[model_name])


#     def predict(self, audio_frame):
#         prediction = self.oww_model.predict(audio_frame)
#         result = prediction[self.model_name] > 0.9
#         if result:
#             self.reset_model()
#         return result
    
#     def reset_model(self):
#         self.oww_model.reset()

class PVAlgorithm(BaseVAAlgorithm):
    def __init__(self, api_key, model_name = "alexa"):
        super().__init__()
        self.model_name = model_name
        self.porcupine = pvporcupine.create(access_key=api_key, keywords=[model_name])

        self.CHUNK = self.porcupine.frame_length
        self.RATE = self.porcupine.sample_rate


    def predict(self, audio_frame):
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, audio_frame)
        result = self.porcupine.process(pcm)
        return result >= 0
    