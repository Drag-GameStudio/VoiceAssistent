from abc import ABC, abstractmethod, ABCMeta
from singleton_models.middleware import middleware_object

class classproperty(object):
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class Singleton(ABCMeta):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class BaseService(ABC, metaclass=Singleton):

    def global_handle(self, **kwargs):
        middleware_object.start_action("run_module")
        result = self.handle(**kwargs)
        middleware_object.start_action("end_module")

        return result

    def handle(self, **kwargs):
        ...

    @classproperty
    def info(cls):
        return """This is base Module"""