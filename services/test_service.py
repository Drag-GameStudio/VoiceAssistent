from .base import BaseService, classproperty

class TestS(BaseService):
    def handle(self, name: str):
        print(name)
        return "name was checked. This is cool gay"

    @classproperty
    def info(cls):
        return """
            This module can search all info by name
            requare key argument: 
            name
        """
    
    