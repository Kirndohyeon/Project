import socket
from collections import deque


class TCPConnect:
    def __init__(self, *, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.socket.close()


class TCPClient(TCPConnect):
    def __init__(self, *, ip, port):
        super(TCPClient, self).__init__()

    def __del__(self):
        super(TCPClient, self).__del__()

    def connect(self):
        self.socket.connect(self.ip, self.port)

    def send_image(self, image_file):
        msg_length = "0" * (9 - int(str(len(image_file)))) + str(len(image_file))
        self.socket.send(msg_length.encode(encoding="utf-8"))
        self.socket.send(image_file)

    def send_string(self, msg):
        msg_length = "0" * (9 - int(str(len(msg)))) + str(len(msg))
        self.socket.send(msg_length.encode(encoding="utf-8"))
        self.socket.send(msg)

    def recv(self):
        data = self.socket.recv(9)
        msg = data.decode()
        read_byte = int(msg)
        return self.socket.recv(read_byte)




class TCPServer(TCPConnect):
    def __init__(self, *, ip, port):
        super(TCPServer, self).__init__()

    def __del__(self):
        super(TCPServer, self).__del__()

    def open(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))

    def listen(self):
        self.socket.listen()
        return self.socket.accept()

    def send_image(self, target_client, image_file):
        msg_length = "0" * (9 - int(str(len(image_file)))) + str(len(image_file))
        target_client.send(msg_length.encode(encoding="utf-8"))
        target_client.socket.send(image_file)

    def send_string(self, msg):
        pass

    def recv(self):
        pass


