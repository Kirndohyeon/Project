import send_recv

socket = send_recv.TcpConnect(ip="localhost", port=17392)
socket.server_open()

client, _ = socket.server_listen()
socket.send_image(socket.server_recv(client))

print("Work done.")
