from abc import ABC, abstractmethod


class classproperty(object):
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class BaseService(ABC):
    @abstractmethod
    def handle(self, **kwargs):
        ...

    @classproperty
    def info(cls):
        return """This is base Module"""