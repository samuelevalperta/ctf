import socket

ip = "192.168.1.3"
port = 2000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ip, port)
s.bind(server_address)
print("Ctrl+c per chiudere il server")

while True:
    print("Server in ascolto")
    data, address = s.recvfrom(4096)
    print("\n\n Server ricevuto: ", data.decode('utf-8'), "\nn")
    