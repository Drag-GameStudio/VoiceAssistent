from .base import BaseEngine
from groq import Groq
from .promts import general_prompt_create
from singleton_models.middleware import middleware_object
from data_base.dialogs.models import Dialog



class History():
    MAX_HISTORY = 10
    def __init__(self, system_prompt: str = ""):
        self.history = []
        self.system_prompt = system_prompt
        if system_prompt is not None:
            self.add_to_history("system", system_prompt, with_db=False)
        self.load_dialog()
        


    def load_dialog(self):
        all_dialogs = list(Dialog.objects.all().order_by("-id"))[:self.MAX_HISTORY]
        all_dialogs.reverse()
        for dialog in all_dialogs:
            self.add_to_history(dialog.role, dialog.content, with_db=False)


    def add_to_history(self, role: str, content: str, with_db: bool = True):
        self.history.append({
            "role": role,
            "content": content
        })
        if with_db:
            Dialog.objects.create(
                role=role,
                content=content
            )
        if len(self.history) - 1 > self.MAX_HISTORY:
            self.history.pop(1)
        

class LLMModel(BaseEngine):
    def __init__(self, api_key: str, 
                 model_name: str = "openai/gpt-oss-120b", 
                 history: History = History(general_prompt_create("ru", "")),
                 ):
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
        self.client = Groq(api_key=self.api_key)

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
            return e
