from .base import BaseVAAlgorithm
import openwakeword
openwakeword.utils.download_models()


class OWKAlgorithm(BaseVAAlgorithm):

    def __init__(self, model_name = "alexa" ):
        super().__init__()
        self.model_name = model_name
        self.oww_model = openwakeword.Model(wakeword_models=[model_name])


    def predict(self, audio_frame):
        prediction = self.oww_model.predict(audio_frame)
        result = prediction[self.model_name] > 0.9
        if result:
            self.reset_model()
        return result
    
    def reset_model(self):
        self.oww_model.reset()