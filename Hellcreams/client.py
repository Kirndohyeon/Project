import send_recv

socket = send_recv.TCPClient(ip="localhost", port=17392)
socket.connect()

f = open("./send_client_image.jpg", "rb")
data = f.read()
socket.send_image(data)
f.close()

a = socket.recv()
f = open("./recv_client_image.jpg", "wb")
f.write(a)
f.close()