import socket
import random

# ฟังก์ชันสำหรับตัดสินผลเป่ายิงฉุบ
def decide_winner(choice1, choice2):
    outcomes = {
        ("rock", "scissors"): "Player wins!",
        ("scissors", "rock"): "Server wins!",
        ("scissors", "paper"): "Player wins!",
        ("paper", "scissors"): "Server wins!",
        ("paper", "rock"): "Player wins!",
        ("rock", "paper"): "Server wins!",
    }
    if choice1 == choice2:
        return "It's a tie!"
    return outcomes.get((choice1, choice2), "Invalid choices!")

# ตั้งค่าการเชื่อมต่อ
host = socket.gethostbyname(socket.gethostname())  # ใช้ IP เครื่องของ Host
port = 1000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)  # รับการเชื่อมต่อทีละ 1 Client

print(f"Server started on {host}:{port}")

while True:
    print("Waiting for a client to connect...")
    client_socket, client_addr = server.accept()
    print(f"Client connected from {client_addr}")

    try:
        # รับตัวเลือกจาก Client
        client_socket.send("Enter your choice (rock, paper, scissors): ".encode())
        player_choice = client_socket.recv(1024).decode().strip().lower()
        print(f"Player chose: {player_choice}")

        # Server เลือกตัวเลือกของตัวเองแบบสุ่ม
        server_choice = random.choice(["rock", "paper", "scissors"])
        print(f"Server chose: {server_choice}")

        # ตัดสินผลและส่งผลลัพธ์กลับไปยัง Client
        result = decide_winner(player_choice, server_choice)
        final_result = (
            f"Player chose: {player_choice}\n"
            f"Server chose: {server_choice}\n"
            f"Result: {result}"
        )
        client_socket.send(final_result.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()