import socket
import threading

# Winner decide function.
def decide_winner(choice1, choice2):
    outcomes = {
        ("rock", "scissors"): "Player 1 wins!",
        ("rock", "paper"): "Player 2 wins!",
        ("scissors", "paper"): "Player 1 wins!",
        ("scissors", "rock"): "Player 2 wins!",
        ("paper", "rock"): "Player 1 wins!",
        ("paper", "scissors"): "Player 2 wins!",
    }
    if choice1 == choice2:
        return "It's a tie!"
    return outcomes.get((choice1, choice2), "Invalid choices!")

# Client handle function.
def handle_client(client_socket, client_addr, player_number):
    print(f"Client connected from {client_addr} as Player {player_number}")
    try:
        # Annouce Client that Client is a player 1 or player 2.
        client_socket.send(f"You are Player {player_number}".encode())
        
        # Receive data from Client.
        player_choice = client_socket.recv(1024).decode().strip().lower()
        print(f"Player {player_number} chose: {player_choice}")
        
        # Save player choice.
        choices[player_number - 1] = player_choice
        
        # Wait for 2 Client chose.
        while None in choices:
            pass
        
        # Send result back to Client.
        result = decide_winner(choices[0], choices[1])
        final_result = (
            f"Player 1 chose: {choices[0]}\n"
            f"Player 2 chose: {choices[1]}\n"
            f"Result: {result}"
        )
        client_socket.send(final_result.encode())
    except Exception as e:
        print(f"Error with Player {player_number}: {e}")
    finally:
        client_socket.close()
        
# Connection setting.
host = socket.gethostbyname(socket.gethostname())
port = 1000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2) # Wait for connection from 2 Client.

print(f"Server started on {host}:{port}")
players = []
choices = [None, None] # Choice from player 1 and player 2.

# Wait for connection from Client.
while len(players) < 2:
    client_socket, client_addr = server.accept()
    player_number = len(players) + 1
    players.append(client_socket)
    thread = threading.Thread(target=handle_client, args=(client_socket, client_addr, player_number))
    thread.start()
    
# Close server after end game.
server.close()