import ctypes
from pathos.helpers import mp as multiprocessing
import threading
from voice_activation.va_manage import VAManager



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

import time

def run_multi_va_and_task(request, va_manager: VAManager, run_func):
    task_process = multiprocessing.Process(target=run_func, args=(request,))
    va_process = multiprocessing.Process(target=va_manager.listen_micro)
    va_process.start()
    task_process.start()

    while True:
        if not task_process.is_alive():
            print("Задача (task_thread) завершена. Останавливаю микрофон...")
            va_process.terminate()  # Жёстко убиваем процесс микрофона
            task_process.join()
            task_process.terminate()
            break
        
        if not va_process.is_alive():
            print("Микрофон перестал слушать сам.")
            task_process.terminate()

            break
        
        time.sleep(0.1)
    