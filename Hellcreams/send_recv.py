import socket


class TCPConnect:
    def __init__(self, *, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.socket.close()


class TCPClient(TCPConnect):
    def __init__(self, *, ip, port):
        super().__init__(ip=ip, port=port)

    def __del__(self):
        super().__del__()

    def connect(self):
        self.socket.connect((self.ip, self.port))

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
        super().__init__(ip=ip, port=port)
        self.client_conn = None
        self.client_addr = None

    def __del__(self):
        super().__del__()

    def open(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))

    def listen(self):
        self.socket.listen()
        self.client_conn, self.client_addr = self.socket.accept()

    def send_image(self, image_file):
        msg_length = "0" * (9 - int(str(len(image_file)))) + str(len(image_file))
        self.client_conn.send(msg_length.encode(encoding="utf-8"))
        self.client_conn.send(image_file)

    def send_string(self, msg):
        msg_length = "0" * (9 - int(str(len(msg)))) + str(len(msg))
        self.client_conn.send(msg_length.encode(encoding="utf-8"))
        self.client_conn.send(msg)

    def recv(self):
        data = self.client_conn.recv(9)
        msg = data.decode()
        read_byte = int(msg)
        return self.client_conn.recv(read_byte)

