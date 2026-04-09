import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 65432))

client.sendall(b"Hello from the client!")
response = client.recv(1024)
print(f"Server said: {response.decode()}")

client.close()
