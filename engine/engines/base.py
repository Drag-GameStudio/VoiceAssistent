from process_control.init_control import MultiProccessActivation

class BaseEngine(MultiProccessActivation):
    def handle(self, request):
        self.init_preccessing()
        ...

