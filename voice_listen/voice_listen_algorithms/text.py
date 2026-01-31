from .base import VLABase


class VLAText(VLABase):
    def __init__(self, *args):
        super().__init__(*args)

    def listen_micro(self):
        while True:
            text = input("Enter: ")
            self.handler_func(text)