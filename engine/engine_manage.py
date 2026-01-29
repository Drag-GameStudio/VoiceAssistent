from groq import Groq, AsyncGroq
import random
MODELS_NAME = ["openai/gpt-oss-120b",  "llama-3.3-70b-versatile",  "openai/gpt-oss-safeguard-20b"]


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

class ParentModel():
    def __init__(self, api_key="", history: History = History(), use_random: bool = True):
        self.history = history
        self.api_key = api_key

        self.current_model_index = 0
        models_copy = MODELS_NAME.copy()
        if use_random:
            random.shuffle(models_copy)
        self.regen_models_name = models_copy


class Model(ParentModel):

    def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        return "answer"
    
    def get_answer_without_history(self, prompt: list[dict[str, str]]) -> str:
        return self.generate_answer(with_history=False, prompt=prompt)

    def get_answer(self, prompt: str) -> str:
        self.history.add_to_history("user", prompt)
        model_answer = self.generate_answer()
        self.history.add_to_history("assistant", model_answer)
        return model_answer


class GPTModel(Model):
    def __init__(self, api_key, history = History(), use_random: bool = True):
        super().__init__(api_key, history, use_random)
        self.client = Groq(api_key=self.api_key)


    def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        if with_history:
            messages = self.history.history
        else:
            messages = prompt
        
        chat_completion = None
        model_name = None

        while True:
            model_name = self.regen_models_name[self.current_model_index]
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model=model_name,

                )
                break
            except Exception as e:
                print(e)
                self.current_model_index = 0 if self.current_model_index + 1 >= len(self.regen_models_name) else self.current_model_index + 1


        result = chat_completion.choices[0].message.content
        return result