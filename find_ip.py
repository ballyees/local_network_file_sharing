import socket
ips = socket.gethostbyname_ex(socket.gethostname())[2]
print("all ip address:", *ips)
print("Listen on ip:", ips[-1])
print("-------"*5)
