import socket

# create a socket (AF_INET = IPv4, SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# FIX: Allow immediate reuse of the port
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to an IP and Port
server.bind(('localhost', 65432))

# Start listening for connections
server.listen()
print("Server is waiting for a connection...")

# Accept a connection (Blocks until a client connects)
connection, address = server.accept()
print(f"Connected by {address}")

# Receive and Send data
data = connection.recv(1024) # Receive up to 1024 bytes
print(f"Received: {data.decode()}")
connection.sendall(b"Hello from the server!")

# Close the connection
connection.close()
