from abc import ABC, abstractmethod
from singleton_models.middleware import middleware_object

class classproperty(object):
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)



class BaseService(ABC):

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