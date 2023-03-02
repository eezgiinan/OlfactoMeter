import pyfirmata


class Olfactometer:
    def __init__(self, port):
        self.port = port
        board = pyfirmata.Arduino(port)
        print(port)

    def print(self, text):
        print('In the Model. Receiving ', text)
