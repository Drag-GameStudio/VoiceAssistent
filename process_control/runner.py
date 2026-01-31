import ctypes
from pathos.helpers import mp as multiprocessing
from voice_activation.va_manage import VAManager
import psutil
import time
import threading

from voice_activation.va_manage import VAManager
from engine.engine_manage import EngineManager
from voice_acting.voice_acting_manage import VActingManager
from service_manager.runner import postprocess_service_handle
from engine.engines.promts import DISCRIBE_ACTION

def kill_child_processes(parent_pid):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    
    # Находим всех "детей" и убиваем их
    children = parent.children(recursive=True)
    for child in children:
        child.terminate()
    
    # Ждем завершения
    psutil.wait_procs(children, timeout=3)

def kill_thread(thread):
    """Принудительно вызывает исключение внутри потока"""
    if not thread.is_alive():
        return
    
    # Отправляем исключение SystemExit в поток по его ID
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), 
        ctypes.py_object(SystemExit)
    )
    
    if res == 0:
        print("Ошибка: неверный ID потока")
    elif res > 1:
        # Если затронуто больше одного потока, нужно откатить (редкий случай)
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), None)
        print("Ошибка при попытке убить поток")

def run_multi_va_and_task(request, va_manager: VAManager, run_func):
    task_process = threading.Thread(target=run_func, args=(request,))
    va_process = multiprocessing.Process(target=va_manager.listen_micro)
    va_process.start()
    task_process.start()

    while True:
        if not task_process.is_alive():
            print("Задача (task_thread) завершена. Останавливаю микрофон...")
            va_process.terminate()  # Жёстко убиваем процесс микрофона
            break
        
        if not va_process.is_alive():
            print("Микрофон перестал слушать сам.")
            # task_process.terminate()
            # kill_child_processes(task_process.pid)
            kill_thread(task_process)

            break
        
        time.sleep(0.1)

def handler_func(request, vacting_manager: VActingManager, e_manager: EngineManager):
    engine_result = e_manager.handle(request)
    is_command, result = postprocess_service_handle(engine_result)
    if is_command:
        prompt = f"{DISCRIBE_ACTION} \n{result}"
        result = e_manager.handle(prompt)
    
    vacting_manager.acting(result)


def create_handler(va_manager, vacting_manager: VActingManager, e_manager: EngineManager):
    def handle_request(request: str):
        return run_multi_va_and_task(request, va_manager, lambda request: handler_func(request, vacting_manager, e_manager))
    
    return handle_request
