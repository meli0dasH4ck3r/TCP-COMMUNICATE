import socket
import threading
import json
import os
import getpass


class ChatClient:
    def __init__(self):
        self.client = None
        self.nickname = None
        self.password = None
        self.stop_thread = False

    def display_menu(self):
        while True:
            os.system('cls||clear')
            option = input("(1) Enter server\n(2) Add server\n")
            if option == '1':
                self.enter_server()
                break
            elif option == '2':
                self.add_server()

    def enter_server(self):
        os.system('cls||clear')
        with open('servers.json', 'r') as f:
            data = json.load(f)

        print('Your servers:', ', '.join(data.keys()))
        server_name = input("Enter the server name: ")

        if server_name not in data:
            print("Server not found!")
            return

        self.nickname = input("Choose Your Nickname: ")
        if self.nickname.lower() == 'admin':
            self.password = getpass.getpass("Enter Admin Password: ")

        ip = data[server_name]["ip"]
        port = data[server_name]["port"]

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

    def add_server(self):
        os.system('cls||clear')
        server_name = input("Enter a name for the server: ")
        server_ip = input("Enter the IP address of the server: ")
        server_port = int(input("Enter the port number of the server: "))

        with open('servers.json', 'r') as f:
            data = json.load(f)

        data[server_name] = {"ip": server_ip, "port": server_port}

        with open('servers.json', 'w') as f:
            json.dump(data, f, indent=4)

    def receive_messages(self):
        while True:
            if self.stop_thread:
                break
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                    next_message = self.client.recv(1024).decode('ascii')
                    if next_message == 'PASS':
                        self.client.send(self.password.encode('ascii'))
                        if self.client.recv(1024).decode('ascii') == 'REFUSE':
                            print("Connection Refused: Wrong Password")
                            self.stop_thread = True
                    elif next_message == 'BAN':
                        print("Connection Refused: You are banned.")
                        self.client.close()
                        self.stop_thread = True
                else:
                    print(message)
            except socket.error:
                print("An error occurred while receiving messages.")
                self.client.close()
                break

    def write_messages(self):
        while True:
            if self.stop_thread:
                break
            try:
                message = f'{self.nickname}: {input("")}'
                if message[len(self.nickname) + 2:].startswith('/'):
                    if self.nickname.lower() == 'admin':
                        if message[len(self.nickname) + 2:].startswith('/kick'):
                            target = message[len(self.nickname) + 2 + 6:]
                            self.client.send(f'KICK {target}'.encode('ascii'))
                        elif message[len(self.nickname) + 2:].startswith('/ban'):
                            target = message[len(self.nickname) + 2 + 5:]
                            self.client.send(f'BAN {target}'.encode('ascii'))
                    else:
                        print("Commands can only be executed by admins!")
                else:
                    self.client.send(message.encode('ascii'))
            except socket.error:
                print("An error occurred while sending a message.")
                self.client.close()
                break

    def start(self):
        self.display_menu()

        if self.client:
            receive_thread = threading.Thread(target=self.receive_messages)
            write_thread = threading.Thread(target=self.write_messages)
            receive_thread.start()
            write_thread.start()


if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.start()
