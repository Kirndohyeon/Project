import send_recv

socket = send_recv.TcpConnect(ip="localhost", port=17392)
socket.client_connect()

f = open("./send_client_image.jpg", "rb")
data = f.read()
socket.send_image(data)
a = socket.client_recv()
print("recv file is", "" if a is None else "not", "None")
