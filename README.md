**Project Title**: VoiceAssistent - Intelligent Voice Assistant for Enhanced User Experience

**Project Goal**: The VoiceAssistent project aims to develop an innovative, event-driven voice assistant that enables users to interact with their environment through voice commands. The primary objective is to provide an intuitive and accessible interface for individuals, particularly those with visual impairments or mobility issues, to control and automate various tasks and devices in their homes. By leveraging cutting-edge technologies and algorithms, VoiceAssistent seeks to revolutionize the way people interact with their surroundings, making their lives more convenient, comfortable, and enjoyable.

**Core Logic & Principles**: The VoiceAssistent system operates on a layered architecture, with a core logic that revolves around continuous spoken command capture, voice activation, and spoken answer synthesis. The system's primary components include:

* **Voice Activation**: The VAManager detects wake-words or commands using PVAlgorithm or VAText, triggering the voice activation process.
* **Speech Recognition**: The VLManager captures user utterances and forwards raw audio to the chosen VoiceListenAlgorithm for processing.
* **LLM Engine**: The EngineManager handles text requests to the LLM engine, which generates answers based on the input prompts.
* **Voice Synthesis**: The VActingManager receives the LLM answer and selects a voice-acting algorithm to synthesize speech, using various APIs such as ElevenLabs or Edge TTS.
* **History Management**: The History component maintains a sliding window of recent turns, persisting dialog history in the Dialog DB.

The system's functional flow involves a series of dependencies, including:

* `manage.py` (entry point) → `PyAudioManager.start_stream()`
* `VAManager.listen_micro()` → `PVAlgorithm.detect()` → `VLManager.listen_micro()` → `VoiceListenAlgorithm.process(audio)`
* `EngineManager.handle(text)` → `GroqLLMEngine.handle()` → `History.add_to_history("user")` → `GroqLLMEngine.generate_answer()` → `History.add_to_history("assistant")`
* `VActingManager.handle(answer)` → `VoiceActingAlgorithm.synthesize()` → `middleware_object.start_action("play_sound")`

**Key Features**:
* Continuous spoken command capture and voice activation
* Advanced speech recognition using VoiceListenAlgorithm
* Integration with LLM engines for answer generation
* Voice synthesis using various APIs (ElevenLabs, Edge TTS, etc.)
* History management with a sliding window of recent turns
* Automation of simple tasks and integration with smart home devices

**Dependencies**:
* `PyAudio` for audio stream management
* `PVAlgorithm` and `VAText` for wake-word/command detection
* `VoiceListenAlgorithm` for speech recognition
* `GroqLLMEngine` for LLM engine integration
* `ElevenLabs` and `Edge TTS` for voice synthesis
* `Google Speech Recognition` and `Google Text-to-Speech` for alternative speech recognition and synthesis
* `IoT device APIs` for smart home device integration
* `SQLite` for Dialog DB management
* Environment variables: `GROQ_API_KEY`, `WORD_API_KEY`, `ELEVEN_API_KEY` required for external services.

## Executive Navigation Tree
* 📄 Core Engine
  * [Documentation](#llmengine-documentation)
  * [Prompts Module](#promts-module-documentation)
  * [Service Manager Overview](#overview-of-service-manager)
  * [Service Manager Documentation](#service-manager-documentation)
  * [Requirements](#requirements)
  * [Example Usage](#example-usage)
* 📂 Service Manager
  * [Project Info](#project-info)
  * [Manager Component](#manager-component)
  * [System Initialization](#system-initialization)
  * [Process Control](#process-control)
  * [Service Manager Components](#service-manager-components)
  * [Service Manager Functional Flow](#service-manager-functional-flow)
  * [Service Manager Technical Logic Flow](#service-manager-technical-logic-flow)
  * [Service Manager Data Contract](#service-manager-data-contract)
* ⚙️ Auto Create Component
  * [Data Contract](#data-contract)
  * [Auto Create Component](#auto-create-component)
  * [Auto Create Component Logic](#auto-create-component-logic)
  * [Auto Create Component Functional Flow](#auto-create-component-functional-flow)
  * [Auto Create Component Technical Logic Flow](#auto-create-component-technical-logic-flow)
  * [Auto Create Component Data Contract](#auto-create-component-data-contract)
  * [Auto Create Component Logic Flow](#auto-create-component-logic-flow)
* 📊 Task Management
  * [Base Service Logic Flow](#base-service-logic-flow)
  * [Task Manager Component Logic Flow](#task-manager-component-logic-flow)
* 📢 Middleware and Music Management
  * [Middleware Component Logic Flow](#middleware-component-logic-flow)
  * [Music Manager Component Logic Flow](#music-manager-component-logic-flow)
* 🌟 Weather and Search
  * [Weather Component Logic Flow](#weather-component-logic-flow)
  * [Auto Search Component Logic Flow](#auto-search-component-logic-flow)
* 🎵 Audio Management
  * [Py Audio Manager Component Logic](#py-audio-manager-component-logic)
  * [Py Audio Manager Data Contract](#py-audio-manager-data-contract)
  * [Play Audio Manager Component Logic](#play-audio-manager-component-logic)
  * [Play Audio Manager Data Contract](#play-audio-manager-data-contract)
* 🧠 Voice Assistant
  * [API Side Vacting Algorithm Component Logic](#api-side-vacting-algorithm-component-logic)
  * [API Side Vacting Algorithm Data Contract](#api-side-vacting-algorithm-data-contract)
  * [Edge Vacting Algorithm Component Logic](#edge-vacting-algorithm-component-logic)
  * [Edge Vacting Algorithm Data Contract](#edge-vacting-algorithm-data-contract)
  * [Google Vacting Algorithm Component Logic](#google-vacting-algorithm-component-logic)
  * [Google Vacting Algorithm Data Contract](#google-vacting-algorithm-data-contract)
* 🗣️ Voice Activation
  * [Voice Assistant Component Logic](#voice-assistant-component-logic)
  * [Voice Activation Data Contract](#voice-activation-data-contract)
  * [Voice Acting Data Contract](#voice-acting-data-contract)
  * [Voice Activation Algorithms Component Logic](#voice-activation-algorithms-component-logic)
* 📝 Voice Text and Listen
  * [PV Algorithm Component Logic](#pvalgorithm-component-logic)
  * [PV Algorithm Data Contract](#pvalgorithm-data-contract)
  * [VA Text Component Logic](#vatext-component-logic)
  * [VA Text Data Contract](#vatext-data-contract)
  * [Voice Listen Algorithms Component Logic](#voice-listen-algorithms-component-logic)
  * [VL Base Component Logic](#vlbase-component-logic)
  * [VL Base Data Contract](#vlbase-data-contract)
* 📞 Cloud and VOSK
  * [VOSK VLA Component Logic](#vosk-vla-component-logic)
  * [VOSK VLA Data Contract](#vosk-vla-data-contract)
  * [Cloud VLA Component Logic](#cloud-vla-component-logic)
  * [Cloud VLA Data Contract](#cloud-vla-data-contract)
  * [Cloud VLA PyAudio Component Logic](#cloud-vla-pyaudio-component-logic)
  * [Cloud VLA PyAudio Data Contract](#cloud-vla-pyaudio-data-contract)
* 📈 VL Manager
  * [VL Manager Logic](#vl-manager-logic)
  * [VL Manager Component Logic](#vl-manager-component-logic)
  * [VL Manager Data Contract](#vl-manager-data-contract)
  * [VLA Text Logic](#vla-text-logic)
  * [VLA Text Data Contract](#vla-text-data-contract)

 

<a name="llmengine-documentation"></a>
## LLM Engine Documentation
The LLM Engine is a crucial component of the VoiceAssistent system, responsible for handling text requests to the LLM engine. This documentation provides a detailed overview of the LLM Engine's functionality, interactions, and technical logic flow.

### Entity Table
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `History` | Class | Manages dialogue history | Stores a maximum of 10 turns |
| `LLMModel` | Class | Base LLM model | Handles user requests and generates answers |
| `GroqLLMEngine` | Class | Groq-specific LLM engine | Utilizes the Groq API for chat completions |
| `api_key` | String | Groq API key | Required for Groq API authentication |
| `model_name` | String | LLM model name | Defaults to "openai/gpt-oss-120b" |
| `request` | String | User input | Passed to the LLM engine for processing |
| `response` | String | LLM engine output | Returned to the user as a spoken answer |

### Technical Logic Flow
1. The `History` class is initialized with a system prompt and loads the dialogue history from the database.
2. The `LLMModel` class is initialized with an API key, model name, and history object.
3. The `handle` method of `LLMModel` is called with a user request, which adds the request to the history and generates an answer using the `generate_answer` method.
4. The `GroqLLMEngine` class overrides the `generate_answer` method to utilize the Groq API for chat completions.
5. The `GroqLLMEngine` class handles exceptions and triggers an error action using the `middleware_object`.

### Interactions
* The LLM Engine interacts with the `middleware_object` to trigger actions, such as error handling.
* The LLM Engine interacts with the `History` class to manage dialogue history.
* The LLM Engine interacts with the Groq API to generate answers.

### Visible Interactions
* The LLM Engine receives user requests from the `EngineManager` class.
* The LLM Engine returns answers to the `EngineManager` class, which are then passed to the `VActingManager` for speech synthesis.

### Critical Constraints
* The `api_key` is required for Groq API authentication.
* The `model_name` defaults to "openai/gpt-oss-120b" if not specified.
* The `History` class stores a maximum of 10 turns.

### Code Structure
The LLM Engine code is organized into the following modules:
* `llm_engine.py`: Contains the `LLMModel` and `GroqLLMEngine` classes.
* `base.py`: Contains the `BaseEngine` class, which is inherited by `LLMModel`.
* `promts.py`: Contains the `general_prompt_create` function, which is used to create a system prompt.
* `middleware.py`: Contains the `middleware_object`, which is used to trigger actions. 
<a name="promts-module-documentation"></a>
## Prompts Module Documentation
### Overview of Prompts
The `promts.py` module contains functions for creating and managing prompts for the voice assistant. The primary function, `general_prompt_create`, generates a prompt based on the language and identify prompt provided.

### Entity Table
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `DEFAULT_ASSISTENT_PROMPT` | String | Default prompt | Contains the base rules for the voice assistant's responses |
| `general_prompt_create` | Function | Prompt creation | Returns a final prompt based on language and identify prompt |
| `languange` | Parameter | Language specification | Specifies the language for the prompt |
| `identify_prompt` | Parameter | Identify prompt | Provides additional context for the prompt |

### Functionality
The `general_prompt_create` function takes two parameters: `languange` and `identify_prompt`. It returns a final prompt that includes the default assistant prompt, language specification, identify prompt, and modules prompt.

### Code Snippet
```python
def general_prompt_create(languange, identify_prompt):
    final_prompt = f"""
        {DEFAULT_ASSISTENT_PROMPT} \n
        all answers have to be in {languange}
        {identify_prompt} \n
        {get_prompt_for_modules()}
    """
    return final_prompt
```

### Identify Prompts
The module also contains predefined identify prompts for specific personas, such as `DONATIK_ID` and `ALEXA_ID`. These prompts provide additional context and rules for the voice assistant's responses.

### Discribe Action
The `DISCRIBE_ACTION` variable contains a prompt for describing the output to the user. It instructs the voice assistant to provide a direct answer to the user's question without discussing the status of the action or the output. The description must follow the base instructions provided in the identify prompt.

### Example Use Case
To create a prompt for a specific persona, you can call the `general_prompt_create` function with the desired language and identify prompt. For example:
```python
prompt = general_prompt_create("Russian", DONATIK_ID)
print(prompt)
```
This would generate a prompt that includes the default assistant prompt, language specification, and the `DONATIK_ID` identify prompt. 
<a name="service-manager-documentation"></a> Service Manager Documentation
#### 
<a name="overview-of-service-manager"></a> Overview of Service Manager
The Service Manager is a modular system designed to route user requests to specific software modules. It analyzes the user's input, determines the required module, and validates the presence of necessary arguments. If all arguments are provided, it outputs an execution command; otherwise, it asks for the missing information.

#### 
<a name="requirements"></a> Requirements
The requirements for each component are as follows:
#### Auto Create Component
* `groq`
* `subprocess`
* `sys`

#### Auto Search Component
* `ddgs`
* `bs4`
* `requests`

#### Music Manager Component
* `ytmusicapi`
* `yt_dlp`
* `sounds`

### 
<a name="example-usage"></a> Example Usage
To use the VLManager and VLAText classes, simply create instances and call the corresponding methods:
```python
# VLManager
vla = VLAText()
vl_manager = VLManager(vla)
vl_manager.listen_micro()

# VLAText
vla_text = VLAText()
vla_text.listen_micro()
```
> Note: The `listen_micro` method of the VLAText class will block until the user enters text. The `listen_micro` method of the VLManager class will start the voice listening process and stop it when the `start_action` method of the `middleware_object` is called with the "stop_listening" action. 
<a name="project-info"></a> Project Info
The project name is **VoiceAssistent**. 

### 
<a name="manager-component"></a>
## Manager Component
The `Manager` class is responsible for orchestrating the voice activation and listening processes. It takes instances of `VAManager` and `VLManager` as parameters in its constructor.

### Visible Interactions
The `Manager` class interacts with the following components:

* `VAManager`: for voice activation
* `VLManager`: for voice listening

### Technical Logic Flow
The `Manager` class has a `start` method that runs an infinite loop, calling the `listen_micro` methods of `VAManager` and `VLManager` in sequence.

### Data Contract
The `Manager` class does not have any explicit inputs or outputs. However, it relies on the following parameters:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `va_manager` | `VAManager` | Voice activation manager |  |
| `vl_manager` | `VLManager` | Voice listening manager |  | 
<a name="system-initialization"></a>
## System Initialization
The system initialization process involves setting up the environment, loading settings, and creating instances of various managers.

### Visible Interactions
The system initialization process interacts with the following components:

* `PyAudioManager`: for managing the audio stream
* `init_modules`: for initializing modules
* `general_prompt_create`: for creating a prompt
* `GroqLLMEngine`: for creating an LLM engine
* `EngineManager`: for creating an engine manager
* `VAManager`: for creating a voice activation manager
* `VActingManager`: for creating a voice acting manager
* `VLManager`: for creating a voice listening manager

### Technical Logic Flow
The system initialization process involves the following steps:

1. Setting up the environment and loading settings
2. Creating instances of `PyAudioManager`, `GroqLLMEngine`, `EngineManager`, `VAManager`, `VActingManager`, and `VLManager`
3. Initializing modules using `init_modules`
4. Creating a prompt using `general_prompt_create`
5. Starting the `Manager` instance

### Data Contract
The system initialization process relies on the following parameters:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `groq_api_key` | `str` | Groq API key |  |
| `word_api_key` | `str` | Word API key |  |
| `eleven_api_key` | `str` | Eleven API key |  |
| `bot_settings` | `dict` | Bot settings |  | 
<a name="process-control"></a>
## Process Control
The process control component is responsible for managing the initialization and termination of processes.

### Visible Interactions
The process control component interacts with the following components:

* `MultiProccessActivation`: for managing process activation

### Technical Logic Flow
The process control component involves the following steps:

1. Checking if the process is initialized
2. Initializing the process using `custom_initialize`
3. Terminating the process using `custom_quite`

### Data Contract
The process control component relies on the following parameters:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `is_initialized` | `bool` | Process initialization flag |  |

## Process Control Component
The process control component is responsible for managing the initialization and termination of processes.

### Visible Interactions
The process control component interacts with the following components:

* `VAManager`: for voice activation
* `VActingManager`: for voice acting
* `EngineManager`: for engine management
* `middleware_object`: for starting actions

### Technical Logic Flow
The process control component involves the following steps:

1. Creating instances of `VAManager`, `VActingManager`, and `EngineManager`
2. Defining a handler function `handler_func` that takes a request, `VActingManager`, and `EngineManager` as parameters
3. Creating a `create_handler` function that returns a `handle_request` function
4. The `handle_request` function calls `run_multi_va_and_task` which starts a `VAManager` instance and a task process
5. The `run_multi_va_and_task` function waits for the task process to finish or the `VAManager` instance to terminate

### Data Contract
The process control component relies on the following parameters:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `request` | `str` | Request string |  |
| `va_manager` | `VAManager` | Voice activation manager |  |
| `vacting_manager` | `VActingManager` | Voice acting manager |  |
| `e_manager` | `EngineManager` | Engine manager |  |

### Code Snippet
```python
def run_multi_va_and_task(request, va_manager: VAManager, run_func):
    task_process = threading.Thread(target=run_func, args=(request,))
    va_process = multiprocessing.Process(target=va_manager.listen_micro)
    va_process.start()
    task_process.start()

    while True:
        if not task_process.is_alive():
            va_process.terminate() 
            break
        
        if not va_process.is_alive():
            kill_thread(task_process)

            break
        
        time.sleep(0.1)

    middleware_object.start_action("end_task")
```
### Requirements
The process control component requires the following libraries:

* `pathos`
* `multiprocessing`
* `psutil`
* `ctypes`
* `threading`
* `time`

Note: The requirements are based on the provided `requirements.txt` file.

### 
<a name="service-manager-components"></a> Service Manager Components
The Service Manager consists of several key components:
* **Initialization Module**: Responsible for initializing the available modules and generating a prompt for the user.
* **Reader Module**: Parses the user's command and extracts the service name and arguments.
* **Runner Module**: Runs the selected service with the provided arguments.

#### 
<a name="service-manager-functional-flow"></a> Service Manager Functional Flow
1. The user provides input to the Service Manager.
2. The **Initialization Module** analyzes the input to determine if a specific module is required.
3. If a module is required, the **Reader Module** parses the input to extract the service name and arguments.
4. The **Runner Module** runs the selected service with the provided arguments.
5. If any required arguments are missing, the Service Manager asks the user for the missing information.

#### 
<a name="service-manager-technical-logic-flow"></a> Service Manager Technical Logic Flow
The technical logic flow of the Service Manager is as follows:
```python
# Initialization Module
def init_modules():
    for module_name in INSTALLED_APPS:
        curr_cls = get_cls_module(module_name)
        curr_cls()

# Reader Module
def read_command(command: str):
    splited_comand = command.split("|")
    service_name = splited_comand[0]
    kwargs = {}
    for key_args in splited_comand[1:]:
        key = key_args.split("=")[0]
        value = "".join(re.split(r'([=])', key_args)[1:])
        value = value[2:len(value) - 1]
        kwargs[key] = value

    return service_name, kwargs

# Runner Module
def run_service(service_name: str, kwargs: dict):
    cls = get_cls_module(service_name)    
    cls_object = cls()
    return cls_object.global_handle(**kwargs)
```

#### 
<a name="service-manager-data-contract"></a> Service Manager Data Contract
The data contract for the Service Manager is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `service_name` | `str` | Input | The name of the service to run |
| `kwargs` | `dict` | Input | The arguments for the service |
| `result` | `str` | Output | The result of the service execution |

#### 
<a name="data-contract"></a> Data Contract
The data contract for each component is as follows:
#### Task Manager Component
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `type_of_action` | `str` | Input | The type of action to perform (e.g., get_tasks, add_task, etc.) |
| `tasks` | `list` | Output | A list of tasks retrieved from the Todoist API |
| `task_id` | `int` | Input | The ID of the task to complete or delete |
| `content` | `str` | Input | The content of the task to add |

#### Weather Component
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `city_name` | `str` | Input | The name of the city to retrieve weather information for |
| `weather` | `dict` | Output | A dictionary containing the current weather information |

#### Middleware Component
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `action_name` | `str` | Input | The name of the action to perform (e.g., end_listen, activate_by_word, etc.) |

### 
<a name="auto-create-component"></a>
## Auto Create Component
The Auto Create component is a part of the VoiceAssistent system, responsible for generating Python code based on user input. It utilizes the Groq API to interact with the OpenAI GPT-3 model, which generates code based on the provided prompt.

### 
<a name="auto-create-component-logic"></a> Auto Create Component Logic
The Auto Create component consists of the following key functions:
* `install_package(package)`: Installs a Python package using pip.
* `code_prepearing(raw_answer)`: Prepares the generated code by extracting the code block and installing required libraries.
* `gen_code(what_need)`: Generates Python code using the Groq API and OpenAI GPT-3 model.
* `handle(what_need)`: Executes the generated code and returns the result.

### 
<a name="auto-create-component-functional-flow"></a> Auto Create Component Functional Flow
1. The user provides input to the Auto Create component.
2. The `handle(what_need)` function is called, which generates Python code using the `gen_code(what_need)` function.
3. The generated code is prepared using the `code_prepearing(raw_answer)` function.
4. The prepared code is executed using the `exec()` function.
5. The result of the execution is returned.

### 
<a name="auto-create-component-technical-logic-flow"></a> Auto Create Component Technical Logic Flow
The technical logic flow of the Auto Create component is as follows:
```python
def install_package(package):
    # Install a Python package using pip
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def code_prepearing(raw_answer):
    # Prepare the generated code by extracting the code block and installing required libraries
    code_start = raw_answer.find("CODE:")
    if raw_answer[:10].find("LIBS:") != -1:
        libs = raw_answer[5:code_start].split(",")
        for lib in libs:
            install_package(lib)
    code = raw_answer[code_start + 5:]
    return code

def gen_code(what_need):
    # Generate Python code using the Groq API and OpenAI GPT-3 model
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
    # ... (rest of the code remains the same)
```

### 
<a name="auto-create-component-data-contract"></a> Auto Create Component Data Contract
The data contract for the Auto Create component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `what_need` | `str` | Input | The task description and required parameters |
| `raw_answer` | `str` | Output | The generated Python code |
| `result` | `dict` | Output | The result of the code execution |

### 
<a name="auto-create-component-logic-flow"></a> Auto Create Component Logic Flow
The Auto Create component is responsible for generating Python code based on a given task description. The logic flow is as follows:
1. The `gen_code` function takes in a `what_need` parameter, which describes the task.
2. The function creates a prompt for the Groq API and OpenAI GPT-3 model.
3. The prompt includes the task description, regulation, output format, and execution result structure.
4. The `code_preparing` function prepares the generated code by extracting the code block and installing required libraries.
5. The `install_package` function installs a Python package using pip.

### 
<a name="base-service-logic-flow"></a> Base Service Logic Flow
The Base Service is an abstract base class that provides a basic structure for services. The logic flow is as follows:
1. The `global_handle` function calls the `handle` function and wraps it with middleware actions.
2. The `handle` function is an abstract method that must be implemented by subclasses.

### 
<a name="task-manager-component-logic-flow"></a> Task Manager Component Logic Flow
The Task Manager component is responsible for managing tasks using the Todoist API. The logic flow is as follows:
1. The `get_tasks` function retrieves a list of tasks from the Todoist API.
2. The `add_task` function adds a new task to the Todoist API.
3. The `complite_task` function completes a task on the Todoist API.
4. The `del_task` function deletes a task from the Todoist API.
5. The `handle` function is the main entry point for the Task Manager component, which calls the corresponding function based on the `type_of_action` parameter.

## 
<a name="middleware-component-logic-flow"></a> Middleware Component Logic Flow
The Middleware component is responsible for playing sounds for various actions. The logic flow is as follows:
1. The `end_listen` function plays a sound when listening ends.
2. The `activate_by_word` function plays a sound when activated by a word.
3. The `stop_listening` function plays a sound when listening stops.
4. The `on_error` function plays a sound when an error occurs.
5. The `end_task` function plays a sound when a task ends.
6. The `run_module` function plays a sound when a module is run.
7. The `end_module` function plays a sound when a module ends.
8. The `start_action` function plays a sound for a given action.

### 
<a name="music-manager-component-logic-flow"></a> Music Manager Component Logic Flow
The Music Manager component is responsible for searching and playing music on YouTube Music. The logic flow is as follows:
1. The `search_and_get_url` function takes in a `query` parameter and searches for a song on YouTube Music using the YTMusic API.
2. The function returns the URL of the song or None if not found.
3. The `download_from_ytm` function takes in a `url` parameter and downloads the song using yt_dlp.
4. The `handle` function takes in a `song_name` parameter, searches for the song, downloads it, and plays it using the PlayAudioManager.

### 
<a name="weather-component-logic-flow"></a> Weather Component Logic Flow
The Weather component is responsible for retrieving weather information using the python_weather library. The logic flow is as follows:
1. The `get_weather` function retrieves the current weather for a given city.
2. The `handle` function is the main entry point for the Weather component, which calls the `get_weather` function and returns the result.

## 
<a name="auto-search-component-logic-flow"></a> Auto Search Component Logic Flow
The Auto Search component is responsible for searching information on the internet. The logic flow is as follows:
1. The `fast_search` function takes in a `query` parameter and uses the DDGS API to search for results.
2. The function returns a dictionary with the search results or an error message.
3. The `get_page_content` function takes in a `url` parameter and retrieves the page content using BeautifulSoup.
4. The function removes unnecessary elements, extracts text from headings and paragraphs, and returns the text.

### 
<a name="py-audio-manager-component-logic"></a> Py Audio Manager Component Logic
The PyAudioManager component is responsible for managing the audio stream. The logic flow is as follows:
1. The `start_stream` function starts the audio stream.
2. The `stop_stream` function stops the audio stream.
3. The `get_current_stream_info` function retrieves information about the current audio stream.
4. The `get_index` function retrieves the index of the default input device.

### 
<a name="py-audio-manager-data-contract"></a> Py Audio Manager Data Contract
The data contract for the PyAudioManager component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `args` | `tuple` | Input | Arguments to pass to the `open` method of the PyAudio object |
| `kwargs` | `dict` | Input | Keyword arguments to pass to the `open` method of the PyAudio object |
| `stream` | `PyAudioStream` | Output | The audio stream object |
| `info` | `dict` | Output | Information about the current audio stream |

## 
<a name="play-audio-manager-component-logic"></a> Play Audio Manager Component Logic
The PlayAudioManager component is responsible for playing sounds. The logic flow is as follows:
1. The `get_file_path` function retrieves the file path of a sound.
2. The `play_sound_process` function plays a sound using the Pygame library.
3. The `play_sound` function plays a sound, optionally in a separate thread.

### 
<a name="play-audio-manager-data-contract"></a> Play Audio Manager Data Contract
The data contract for the PlayAudioManager component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `sound_name` | `str` | Input | The name of the sound to play |
| `file_path` | `str` | Input | The file path of the sound to play |
| `is_thread` | `bool` | Input | Whether to play the sound in a separate thread |
| `with_daemon` | `bool` | Input | Whether to set the thread as a daemon |

## 
<a name="api-side-vacting-algorithm-component-logic"></a> Api Side VActing Algorithm Component Logic
The ApiSideVActingAlgorithm component is responsible for generating sound using the ElevenLabs API. The logic flow is as follows:
1. The `gen_sound` function generates sound using the ElevenLabs API.

### 
<a name="api-side-vacting-algorithm-data-contract"></a> Api Side VActing Algorithm Data Contract
The data contract for the ApiSideVActingAlgorithm component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `id` | `int` | Input | An identifier for the sound generation request |
| `request` | `str` | Input | The text to convert to speech |
| `file_path` | `str` | Output | The file path of the generated sound |

## 
<a name="edge-vacting-algorithm-component-logic"></a> Edge VActing Algorithm Component Logic
The EdgeVActingAlgorithm component is responsible for generating sound using the Edge TTS API. The logic flow is as follows:
1. The `acting` function generates sound using the Edge TTS API.

### 
<a name="edge-vacting-algorithm-data-contract"></a> Edge VActing Algorithm Data Contract
The data contract for the EdgeVActingAlgorithm component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `request` | `str` | Input | Text to convert to speech |
| `voice` | `str` | Input | Voice to use for speech synthesis |
| `file_path` | `str` | Output | File path of the generated sound |

## 
<a name="google-vacting-algorithm-component-logic"></a> Google VActing Algorithm Component Logic
The GoogleVActingAlgorithm component is responsible for generating sound using the Google Text-to-Speech API. The logic flow is as follows:
1. The `gen_sound` function generates sound using the Google Text-to-Speech API.
2. The `play_sound_by_id` function plays the generated sound.

### 
<a name="google-vacting-algorithm-data-contract"></a> Google VActing Algorithm Data Contract
The data contract for the GoogleVActingAlgorithm component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `id` | `int` | Input | Identifier for the sound generation request |
| `request` | `str` | Input | Text to convert to speech |
| `file_path` | `str` | Output | File path of the generated sound |

## 
<a name="voice-assistant-component-logic"></a> Voice Assistant Component Logic
The Voice Assistant component is responsible for managing voice activation and voice acting. The logic flow is as follows:
1. The `VAManager` component listens for voice activation using the `listen_micro` function.
2. Once voice activation is detected, the `VActingManager` component is triggered to perform voice acting using the `acting` function.

### 
<a name="voice-activation-data-contract"></a> Voice Activation Data Contract
The data contract for the Voice Activation component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `audio_frame` | `bytes` | Input | Audio frame to process for voice activation |
| `activated` | `bool` | Output | Whether voice activation is detected |

### 
<a name="voice-acting-data-contract"></a> Voice Acting Data Contract
The data contract for the Voice Acting component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `request` | `str` | Input | Text to convert to speech |
| `file_path` | `str` | Output | File path of the generated sound |

## 
<a name="voice-activation-algorithms-component-logic"></a> Voice Activation Algorithms Component Logic
The voice activation algorithms are responsible for detecting the wake-word or command in the audio stream. The logic flow is as follows:
1. The `PVAlgorithm` class uses the Porcupine API to detect the wake-word.
2. The `VAText` class is a placeholder for text-based voice activation.

### 
<a name="pvalgorithm-component-logic"></a> PVAlgorithm Component Logic
The PVAlgorithm component is responsible for detecting the wake-word using the Porcupine API. The logic flow is as follows:
1. The `predict` method takes an audio frame as input and returns a boolean indicating whether the wake-word is detected.
2. The `custom_initialize` method initializes the Porcupine API with the access key and keyword.
3. The `quite_proccessing` method releases the resources used by the Porcupine API.

### 
<a name="pvalgorithm-data-contract"></a> PVAlgorithm Data Contract
The data contract for the PVAlgorithm component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `audio_frame` | `bytes` | Input | Audio frame to process for voice activation |
| `api_key` | `str` | Input | Access key for the Porcupine API |
| `model_name` | `str` | Input | Name of the wake-word model |
| `result` | `bool` | Output | Whether the wake-word is detected |

### 
<a name="vatext-component-logic"></a> VAText Component Logic
The VAText component is a placeholder for text-based voice activation. The logic flow is as follows:
1. The `predict` method takes an audio frame as input and returns a boolean indicating whether the wake-word is detected.
2. The `predict` method is currently not implemented and returns False.

### 
<a name="vatext-data-contract"></a> VAText Data Contract
The data contract for the VAText component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `audio_frame` | `bytes` | Input | Audio frame to process for voice activation |
| `result` | `bool` | Output | Whether the wake-word is detected |

## 
<a name="voice-listen-algorithms-component-logic"></a> Voice Listen Algorithms Component Logic
The voice listen algorithms are responsible for capturing the user's utterance and forwarding it to the voice processing pipeline. The logic flow is as follows:
1. The `VLABase` class provides a base implementation for voice listen algorithms.
2. The `listen_micro` method is an abstract method that must be implemented by concrete voice listen algorithms.

### 
<a name="vlbase-component-logic"></a> VLABase Component Logic
The VLABase component is the base class for voice listen algorithms. The logic flow is as follows:
1. The `__init__` method initializes the voice listen algorithm with a handler function.
2. The `listen_micro` method is an abstract method that must be implemented by concrete voice listen algorithms.
3. The `end_listen` method sends a signal to end the listening process.

### 
<a name="vlbase-data-contract"></a> VLABase Data Contract
The data contract for the VLABase component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `handler_func` | `function` | Input | Handler function for the voice listen algorithm |
| `request` | `str` | Input | Utterance captured by the voice listen algorithm |

## 
<a name="vosk-vla-component-logic"></a> VoskVLA Component Logic
The VoskVLA component is a voice listen algorithm that uses the Vosk API for speech recognition. The logic flow is as follows:
1. The `__init__` method initializes the VoskVLA instance with a language model and a recognizer.
2. The `configurate` method configures the PyAudio stream for audio input.
3. The `listen_micro` method listens to the audio input and recognizes speech using the Vosk API.

### 
<a name="vosk-vla-data-contract"></a> VoskVLA Data Contract
The data contract for the VoskVLA component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `audio_frame` | `bytes` | Input | Audio frame to process for speech recognition |
| `lang` | `str` | Input | Language model for speech recognition |
| `result` | `dict` | Output | Speech recognition result |

### 
<a name="cloud-vla-component-logic"></a> CloudVLA Component Logic
The CloudVLA component is a voice listen algorithm that uses the Google Cloud Speech-to-Text API for speech recognition. The logic flow is as follows:
1. The `__init__` method initializes the CloudVLA instance with a language model and a recognizer.
2. The `prep` method prepares the microphone for audio input.
3. The `listen_micro` method listens to the audio input and recognizes speech using the Google Cloud Speech-to-Text API.

### 
<a name="cloud-vla-data-contract"></a> CloudVLA Data Contract
The data contract for the CloudVLA component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `audio_frame` | `bytes` | Input | Audio frame to process for speech recognition |
| `lang` | `str` | Input | Language model for speech recognition |
| `result` | `dict` | Output | Speech recognition result |

### 
<a name="cloud-vla-pyaudio-component-logic"></a> CloudVLAPyAudio Component Logic
The CloudVLAPyAudio component is a voice listen algorithm that uses the PyAudio library for audio input and the Google Cloud Speech-to-Text API for speech recognition. The logic flow is as follows:
1. The `__init__` method initializes the CloudVLAPyAudio instance with a language model and a recognizer.
2. The `get_rms` method calculates the RMS value of an audio frame.
3. The `recognize_text` method recognizes speech from an audio frame using the Google Cloud Speech-to-Text API.
4. The `listen_micro` method listens to the audio input and recognizes speech using the `recognize_text` method.

### 
<a name="cloud-vla-pyaudio-data-contract"></a> CloudVLAPyAudio Data Contract
The data contract for the CloudVLAPyAudio component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `audio_frame` | `bytes` | Input | Audio frame to process for speech recognition |
| `lang` | `str` | Input | Language model for speech recognition |
| `result` | `dict` | Output | Speech recognition result |

### 
<a name="vl-manager-logic"></a> VLManager Logic
The VLManager class is responsible for managing the voice listening process. It takes a VLABase instance as an argument in its constructor.

### 
<a name="vl-manager-component-logic"></a> VLManager Component Logic
The logic flow is as follows:
1. The `__init__` method initializes the VLManager instance with a VLABase instance.
2. The `listen_micro` method configures the VLABase instance with a PyAudioManager instance and starts the voice listening process.
3. The `listen_micro` method also stops the listening process by calling the `start_action` method of the `middleware_object` with the "stop_listening" action.

### 
<a name="vl-manager-data-contract"></a> VLManager Data Contract
The data contract for the VLManager component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `vla` | `VLABase` | Input | VLABase instance to use for voice listening |
| `py_audio` | `PyAudio` | Input | PyAudio instance to use for audio input |

### 
<a name="vla-text-logic"></a> VLAText Logic
The VLAText class is a voice listen algorithm that uses text input for speech recognition. The logic flow is as follows:
1. The `__init__` method initializes the VLAText instance.
2. The `listen_micro` method listens to text input and calls the `handler_func` method with the input text.

### 
<a name="vla-text-data-contract"></a> VLAText Data Contract
The data contract for the VLAText component is as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `text` | `str` | Input | Text input to process for speech recognition |
| `handler_func` | `function` | Input | Function to call with the text input |

### 
