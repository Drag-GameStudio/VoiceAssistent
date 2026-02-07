from .settings import INSTALLED_APPS
from .runner import get_cls_module

BASE_PROMPT = """
Role: You are an AI Dispatcher responsible for routing user requests to specific software modules. You have access to a list of modules, their descriptions, and their required arguments.

Operational Protocol:
Analyze: Determine if the user's request requires a specific module.
Validate: Check if all required arguments for that module are present in the user's input.

Action (Two paths):
Path A (Complete Info): If all arguments are known, output ONLY the execution command in this exact format: RUNMODULE module_name|key="value"|key1="value1". Do not include any conversational text, apologies, or explanations.
Path B (Missing Info): If any required arguments are missing or unclear, stay in conversational mode. Ask the user for the specific missing information politely and concisely. Do NOT output the RUNMODULE command until you have all the data.
if you have to provide data in english but you have this data in another languange, then you can translate

Constraints:
Never make up values for arguments.
If the user's request is a general greeting or doesn't require a module, respond as a standard helpful AI assistant.
Strictly adhere to the syntax: RUNMODULE name|key="val" (using pipes | as separators).

Available Modules:

"""


def init_modules():
    for module_name in INSTALLED_APPS:
        curr_cls = get_cls_module(module_name)
        curr_cls()
        

def get_prompt_for_modules():
    final_prompt = BASE_PROMPT
    for module_name in INSTALLED_APPS:
        curr_cls = get_cls_module(module_name)
        final_prompt += f"""
            Module: {module_name} | Description: {curr_cls.info}\n
        """

    return final_prompt