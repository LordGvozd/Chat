import socket

code = "utf-8"

# Server data
server_host = socket.gethostbyname(socket.gethostname())
server_port = 7878
#server_ip = "94.228.112.236"
server_ip = socket.gethostbyname(socket.gethostname())

# Client data
client_port = 8787
