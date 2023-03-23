import send_recv
from time import sleep

socket = send_recv.TcpConnect(ip="localhost", port=17392)
socket.client_connect()

socket.send_image("./send_client_image.jpg")
a = socket.client_recv()
print("recv file is", "" if a is None else "not", "None")
