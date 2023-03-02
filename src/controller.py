class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def print(self, text):
        print('In the controller. Propogating', text)
        self.model.print(text)