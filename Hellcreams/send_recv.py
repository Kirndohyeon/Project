import socket

class TcpConnect:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.model = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def client_connect(self):
        if self.model is not None:
            raise ConnectionError("This socket is already " + self.model + ".")

        self.socket.connect((self.ip, self.port))

    def server_open(self):
        if self.model is not None:
            raise ConnectionError("This socket is already " + self.model + ".")

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))

    async def server_listen(self):
        self.socket.listen()
        return self.socket.accept()
