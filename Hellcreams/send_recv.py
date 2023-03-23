import socket

class TcpConnect:
    def __init__(self, *, ip, port):
        self.ip = ip
        self.port = port
        self.model = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.socket.close()

    def client_connect(self):
        if self.model is not None:
            raise ConnectionError("This socket is already " + self.model + ".")

        self.socket.connect((self.ip, self.port))

    def server_open(self):
        if self.model is not None:
            raise ConnectionError("This socket is already " + self.model + ".")

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))

    def server_listen(self):
        self.socket.listen()
        return self.socket.accept()

    def send_image(self, directory):
        f = open(directory, "rb")
        send_image = f.read()
        f.close()
        msg_length = "0" * (9 - int(str(len(send_image)))) + str(len(send_image))

        self.socket.sendall(msg_length.encode(encoding='utf-8'))
        self.socket.sendall(send_image)

    def send_string(self, msg):
        msg_length = "0" * (9 - int(str(len(msg)))) + str(len(msg))
        self.socket.sendall(msg_length.encode(encoding="utf-8"))
        self.socket.sendall(msg)

    def server_recv(self, client_socket):
        data = client_socket.recv(9)
        msg = data.decode()
        read_byte = int(msg)
        return client_socket.recv(read_byte)

    def client_recv(self):
        data = self.socket.recv(9)
        msg = data.decode()
        read_byte = int(msg)
        return self.socket.recv(read_byte)