import services
from services.base import BaseService
from .reader import read_command, check_raw_answer
import importlib

def get_cls_module(service_name: str) -> type[BaseService]:
    mod_part, cls_part = "services." + service_name.rsplit('.', 1)[0], service_name.rsplit('.', 1)[1]
    module = importlib.import_module(mod_part)
    cls = getattr(module, cls_part)

    return cls

def run_service(service_name: str, kwargs: dict):
    cls = get_cls_module(service_name)    
    cls_object = cls()
    return cls_object.global_handle(**kwargs)

def postprocess_service_handle(raw_result) -> tuple[bool, str]:
    status, result = check_raw_answer(raw_result)
    if not status:
        return False, result
    
    service_name, kwargs = read_command(result)
    result = run_service(service_name, kwargs)

    return True, result

if __name__ == "__main__":
    name, kwargs = read_command('test_service.TestS|name="Dima"')
    run_service(name, kwargs)