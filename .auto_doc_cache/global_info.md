## Architecture: VoiceAssistent – Event‑Driven Layered Service  
**Goal:**  A multilingual, witty voice‑assistant that continuously listens, activates on a wake‑word, transcribes speech, queries a LLM (Groq), stores dialog history in SQLite (Django ORM), and speaks the answer.

### Component Logic
* **manage.py**: Bootstrap all singletons, build the processing pipeline, start infinite `Manager.start()` loop.
* **Manager**: Main event loop – coordinates *voice activation* → *voice listening* → *LLM handling*.
* **VAManager**: Detects wake‑word using an algorithm.
* **VLManager**: Captures audio, runs chosen *listen algorithm*, returns raw transcript.
* **EngineManager**: Wraps a concrete `BaseEngine`. Sends transcript, receives answer.
* **VActingManager**: Receives LLM answer, runs *acting algorithm* → audio output.

### Functional Flow (Dependencies)
* `Manager.start()` → `VAManager.listen_micro()` → `VLManager.listen_micro()` → `EngineManager.handle()` → `VActingManager.handle()`
* `EngineManager.handle()` → `GroqLLMEngine.handle()` → `History.add_to_history()` → `Dialog.objects.create()`

### Key Context for Snippets
* `History.history`: Sliding window of last ≤10 messages; fed to Groq API and persisted.
* `middleware_object`: Centralised event dispatcher for error handling, logging, etc.
* `PyAudioManager`: Global audio stream used by activation & listening modules.
* `process_control.runner.create_handler`: Returns a callable that wires **VA → VL → Engine → Acting** together.

### Critical Dependencies for Any Code Edit
* **Django ORM**: `Dialog` model must stay in sync with `History.add_to_history`.
* **Groq SDK**: `GroqLLMEngine.generate_answer` expects `self.client.chat.completions.create(messages=History.history, model=…)`.
* **Singleton middleware**: All error handling and side‑effects rely on `middleware_object.start_action`.
## Architecture: VoiceAssistent (Layered)
**Goal:** Conversational AI with speech recognition, intent identification, and text-to-speech capabilities.

### Component Logic
* **main.py:** Entry point and initialization
* **voice_assistant.py:** User interaction and response generation
* **intent_identifier.py:** Identifies user intent from speech
* **ml_model.py:** Loads and manages pre-trained ML model
* **config.json:** Stores configuration settings

### Functional Flow (Dependencies)
* `main.py` -> `initialize()` -> loads `config.json` -> calls `voice_assistant.py` -> `__init__()`
* `voice_assistant.py` -> `listen()` -> calls `intent_identifier.py` -> `identify_intent()` -> returns intent -> `respond()` -> speaks response
* `intent_identifier.py` -> `identify_intent()` -> uses `ml_model.py` -> `load_ml_model()` -> uses pre-trained model

### Key Context for Snippets
* `config.json` influences speech recognition and text-to-speech functionality
* Shared state: `speech_recognition` and `text_to_speech` objects
* Entry point: `main.py`
* Terminal points: `respond()` and `load_ml_model()`
