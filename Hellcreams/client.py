# 클라이언트 프로그램
# 서버 프로그램은 주피터, 이것은 파이참으로 실행 - 동시에 두개 프로그램 실행을 위해서.
import socket

server_ip = 'localhost'  # 위에서 설정한 서버 ip
server_port = 3333  # 위에서 설정한 서버 포트번호

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((server_ip, server_port))

f = open("./send_client_image.jpg", "rb")
send_image = f.read()
f.close()
msg_length = "0" * (9 - int(str(len(send_image)))) + str(len(send_image))
print(msg_length)

socket.sendall(msg_length.encode(encoding='utf-8'))
socket.sendall(send_image)

data = socket.recv(9)
msg = data.decode()  # 읽은 데이터 디코딩
read_byte = int(msg)
print("expected msg bytes:", read_byte)

data = socket.recv(read_byte)
f = open("./recv_client_image.jpg", "wb")
f.write(data)
f.close()

print("Transmission Complete.")

socket.close()

