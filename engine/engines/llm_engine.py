from .base import BaseEngine
from groq import Groq
from .promts import DEFAULT_ASSISTENT_PROMPT
from singleton_models.middleware import middleware_object


class History:
    def __init__(self, system_prompt: str = ""):
        self.history = []
        if system_prompt is not None:
            self.add_to_history("system", system_prompt)

    def add_to_history(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content
        })

class LLMModel(BaseEngine):
    def __init__(self, api_key: str, model_name: str = "openai/gpt-oss-120b", history: History = History(DEFAULT_ASSISTENT_PROMPT)):
        super().__init__()
        self.history = history
        self.api_key = api_key
        self.model_name = model_name

    
    def generate_answer(self) -> str:
        return "answer"
    
    def handle(self, request: str) -> str:
        super().handle(request)
        self.history.add_to_history("user", request)
        model_answer = self.generate_answer()
        self.history.add_to_history("assistant", model_answer)
        return model_answer

class GroqLLMEngine(LLMModel):

    def __init__(self, *args, **kawargs):
        super().__init__(*args, **kawargs)

    def custom_initialize(self):
        self.client = Groq(api_key=self.api_key)
        super().custom_initialize()
    
    def custom_quite(self):
        del self.client
        return super().custom_quite()

    def generate_answer(self):
        try:
            chat_completion = self.client.chat.completions.create(
                        messages=self.history.history,
                        model=self.model_name,
                    )
            
            result = chat_completion.choices[0].message.content
            return result
            
        except Exception as e:
            print(e)
            middleware_object.start_action("on_error")

            return e[:50]
