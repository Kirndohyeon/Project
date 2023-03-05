import socket
import time
import shutil

host = 'localhost'  # localhost or IPv4 address
port = 3333

# socket.AF_INET: 주소종류 지정(IP) / socket.SOCK_STREAM: 통신종류 지정(UDP, TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen()

client_soc, addr = server_socket.accept()

print('connected client addr:', addr)

# recv(메시지크기): 소켓에서 크기만큼 읽는 함수 / 엔터 누르고 끝나면 나머지는 무시 (C하고 구조가 좀 다른듯)
# 소켓에 읽을 데이터가 없으면 생길 때까지 대기함

# 사진 파일 받기
data = client_soc.recv(9)
msg = data.decode()  # 읽은 데이터 디코딩
read_byte = int(msg)
print("expected msg bytes:", read_byte)

# 파일 저장 (확인용, 필요하지 않으면 지워도 됨)
data = client_soc.recv(read_byte)
f = open("./recv_server_image.jpg", "wb")
f.write(data)
f.close()

# 여기에 가공할 코드 추가하기 (필요에 따라 수정해도 됨)
pass

f = open("./send_server_image.jpg", "wb")
f.write(data)
f.close()

# 가공한 사진 파일 보내기
msg_length = "0" * (9 - int(str(len(data)))) + str(len(data))

client_soc.sendall(msg_length.encode(encoding='utf-8'))
client_soc.sendall(data)

print("Transmission Complete.")

time.sleep(5)
server_socket.close()  # 사용했던 서버 소켓을 닫아줌

