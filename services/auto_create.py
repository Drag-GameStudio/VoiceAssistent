from .base import BaseService, classproperty
from groq import Client
import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

class Auto(BaseService):

    def __init__(self):
        super().__init__()
        self.code_history = []
        self.count_try = 3

    def code_prepearing(self, raw_answer: str):
        code_start = raw_answer.find("CODE:")
        if raw_answer[:10].find("LIBS:") != -1:
            libs = raw_answer[5:code_start].split(",")
            print(libs)
            for lib in libs:
                install_package(lib)
        
        code = raw_answer[code_start + 5:]
        return code

    def gen_code(self, what_need):
        prompt = [
            {
                "role": "system",
                "content": f"""
                ### ROLE
Python Code Generator (Raw Output Mode)

### REGULATION
1. TASK: {what_need}
2. RETURN DATA: A Python dictionary (dict) stored in the variable `result`.

### OUTPUT FORMAT (STRICT)
- IF EXTERNAL LIBRARIES ARE NEEDED: Start with "LIBS:package1,package2" then "CODE:".
- IF ONLY STANDARD LIBRARIES ARE NEEDED: Start with "CODE:".
- NO Markdown (no ```), NO chatty explanations. ONLY raw text.

### EXECUTION & RESULT STRUCTURE (MANDATORY)
The variable `result` MUST be a dictionary and MUST contain:
1. "global_status": (bool) True if the task succeeded, False if an error occurred.
2. "message": (str) "Success" or a detailed error description if global_status is False.
3. [OTHER DATA]: Any other keys required by the task.

The entire logic should be wrapped in a try-except block to ensure the `result` dictionary is always populated even if the main logic fails.

### EXAMPLE STRUCTURE
CODE:
import lib1
import lib2
try:
    # logic here
    result = {{"global_status": True, "message": "Success", "data": 123}}
except Exception as e:
    result = {{"global_status": False, "message": str(e)}}

### INPUT CONTEXT
[INSERT DATA HERE]

### COMMAND
Generate the response now."""
            },
        ]
        for code_his in self.code_history:
            prompt.append({
                "role": "system",
                "content": f"this is your prev code that was incorrect {code_his}"
            })

        if len(self.code_history) > 0:
            prompt.append({
                "role": "system",
                "content": "try to fix it"
            })

        client = Client(api_key="")
        chat_completion = client.chat.completions.create(
                        messages=prompt,
                        model="openai/gpt-oss-safeguard-20b",
                    )
            
        result = chat_completion.choices[0].message.content
        return result

    def handle(self, what_need):
        result_exec = {"status": "error"}
        while True:
            result = self.gen_code(what_need)
            code = self.code_prepearing(result)
            try:
                output_data = {}
                print(code)
                exec(code, {}, output_data)
                result_exec = output_data["result"]
                if result_exec["global_status"] == True or self.count_try <= 0:
                    break
                self.count_try -= 1
                self.code_history.append({
                    "code": code,
                    "error_message": result_exec["message"]
                })
                print(result_exec["message"])
            except Exception as e:
                if self.count_try <= 0:
                    break
                print(e)
                self.count_try -= 1
                self.code_history.append({
                    "code": code,
                    "error_message": e
                })
        
        return result_exec

    @classproperty
    def info(cls):
        return """
            This module can search or do somthing if you cant do it by yourself or you dont have exist modules
            requare key argument: 
            what_need - discribe the task what this code have to do and what parameters it have to return
        """
    
    