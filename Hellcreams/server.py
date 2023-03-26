import send_recv

socket = send_recv.TCPServer(ip="localhost", port=17392)
socket.open()

socket.listen()
a = socket.recv()
socket.send_image(a)

print("Work done.")
