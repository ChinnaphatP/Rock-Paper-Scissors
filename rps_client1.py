import socket

host = input("Enter server IP address: ")
port = int(input("Enter server port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Receive message from server what player you be.
player_info = client.recv(1024).decode()
print(player_info)

# Chose your choice.
choice = input("Enter your choice (rock, paper, scissors): ").strip().lower()
client.send(choice.encode())

# Receive result.
result = client.recv(1024).decode()
print(result)

client.close()