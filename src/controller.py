class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def print(self, text):
        print('In the controller. Propogating', text)
        self.model.print(text)

    def activate_odor(self, odor_number):
        self.model.activate_odor(odor_number)

    def activate_purge(self):
        self.model.activate_purging()

    def activate_rest(self):
        self.model.activate_resting()