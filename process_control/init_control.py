
class MultiProccessActivation:
    is_initialized = False

    def init_preccessing(self):
        if not self.is_initialized:
            self.custom_initialize()
            self.is_initialized = True
            
    def custom_initialize(self):
        ...        

    def custom_quite(self):
        ...

    def quite_proccessing(self):
        if self.is_initialized:
            self.is_initialized = False
            self.custom_quite()

