import socket

host = input("Enter server IP address: ")
port = int(input("Enter server port: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# รับคำแนะนำจาก Server
message = client.recv(1024).decode()
print(message)

# ป้อนตัวเลือกของผู้เล่น
choice = input().strip().lower()
client.send(choice.encode())

# รับผลลัพธ์จาก Server
result = client.recv(1024).decode()
print(result)

client.close()