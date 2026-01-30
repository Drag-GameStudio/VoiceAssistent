from abc import abstractmethod, ABC
from process_control.init_control import MultiProccessActivation


class VLABase(ABC, MultiProccessActivation):

    def __init__(self, handler_func):
        self.handler_func = handler_func

    @abstractmethod
    def listen_micro(self):
        ...

    def configurate(self, p):
        ...

    def send_request(self, request):
        print(f"Send req: {request}")
        self.handler_func(request)