# Part A: Communication Handling (Server) - KHOI
import threading
import socket

class ChatServer:
    def __init__(self, host="127.0.0.1", port=5555):
        # Initialize server and configure socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        self.commands = {
            "KICK": self.kick_command,
            "BAN": self.ban_command
        }
        print("Server is Listening ...")

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client):
        # Handle client's message (could be an admin or regular message)
        while True:
            try:
                msg = client.recv(1024).decode('ascii')
                command, *args = msg.split(" ", 1)
                if command in self.commands:
                    self.commands[command](client, *args)
                else:
                    self.broadcast(msg.encode('ascii'))
            except socket.error:
                self.disconnect_client(client)
                break

    def kick_command(self, client, name):
        # Handle 'kick' command for admin
        if self.is_admin(client):
            self.kick_user(name)
        else:
            client.send('Command Refused!'.encode('ascii'))

    def ban_command(self, client, name):
        # Handle 'ban' command for admin -> add to bans.txt
        if self.is_admin(client):
            self.kick_user(name)
            with open('bans.txt', 'a') as f:
                f.write(f'{name}\n')
            print(f'{name} was banned by the Admin!')
        else:
            client.send('Command Refused!'.encode('ascii'))

    def kick_user(self, name):
        if name in self.nicknames:
            name_index = self.nicknames.index(name)
            client_to_kick = self.clients[name_index]
            self.clients.remove(client_to_kick)
            client_to_kick.send('You Were Kicked from Chat!'.encode('ascii'))
            client_to_kick.close()
            self.nicknames.remove(name)
            self.broadcast(f'{name} was kicked from the server!'.encode('ascii'))

    def disconnect_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            client.close()
            nickname = self.nicknames.pop(index)
            self.broadcast(f'{nickname} left the Chat!'.encode('ascii'))

# Part B: User Connection & Admin Authentication - ANIS
    def receive_clients(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')

            if self.is_banned(nickname):
                client.send('BAN'.encode('ascii'))
                client.close()
                continue

            if nickname == 'admin':
                if not self.authenticate_admin(client):
                    continue

            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f'Nickname of the client is {nickname}')
            self.broadcast(f'{nickname} joined the Chat'.encode('ascii'))
            client.send('Connected to the Server!'.encode('ascii'))

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def is_banned(self, nickname):
        with open('bans.txt', 'r') as f:
            return nickname + '\n' in f.readlines()

    def authenticate_admin(self, client):
        client.send('PASS'.encode('ascii'))
        password = client.recv(1024).decode('ascii')
        if password != 'password123':
            client.send('REFUSE'.encode('ascii'))
            client.close()
            return False
        return True

    def is_admin(self, client):
        return self.nicknames[self.clients.index(client)] == 'admin'

# Part C: Client UI/UX - DAVID
class ClientUI:
    def display_menu(self):
        print("1. Add Server")
        print("2. Exit")

    def add_server(self):
        server_address = input("Enter server address: ")
        server_port = int(input("Enter server port: "))
        return server_address, server_port

    def user_feedback(self, message):
        print(f"[INFO] {message}")

# Part D: Threaded Communication on Client - ENZO
class ClientThread:
    def __init__(self, client):
        self.client = client
        self.running = True

    def receive_messages(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('ascii')
                print(message)
            except socket.error:
                print("Error receiving message")
                self.running = False

    def write_messages(self):
        while self.running:
            try:
                message = input()
                self.client.send(message.encode('ascii'))
            except socket.error:
                print("Error sending message")
                self.running = False

# Part E: Integration & Testing - MADI
if __name__ == "__main__":
    chat_server = ChatServer()
    threading.Thread(target=chat_server.receive_clients).start()
    
    # Placeholder for client integration and testing
