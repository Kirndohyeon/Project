import send_recv

socket = send_recv.TcpConnect(ip="localhost", port=17392)
socket.server_open()

client, _ = socket.server_listen()
a = socket.server_recv(client)
socket.send_image()

print("Work done.")
