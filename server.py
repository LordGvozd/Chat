import socket
import threading
import time

import json_utils
import settings
import crypto


class Chat:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.server = None
        self.run = False

        self.clients = []
        self.nicknames = []
        self.client_keys = []

    # Starting server
    def start(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(10)

        print("Server started")

        self.receive()
        self.run = True

    # Remove client
    def remove_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)

            # Remove client
            self.clients.remove(client)
            client.close()

            # Remove nick
            nick = self.nicknames[index]
            self.nicknames.remove(nick)

            # Remove key
            key = self.client_keys[index]
            self.client_keys.remove(key)

            print("[{}] left the chat".format(nick))
            self.broadcast("[{}] left the chat".format(nick).encode(settings.code))

    # Sending message to all connected client
    def broadcast(self, msg, ignore_client="Not client, string"):
        for client in self.clients:
            try:
                if (client != ignore_client):
                    self.send_message(msg, client)
            except:
                self.remove_client(client)

    # Sending message to one client
    def send_message(self, msg, client):
        encrypted_message = crypto.encrypt(msg, self.get_key_by_client(client))

        client.send(encrypted_message.encode(settings.code))

    # Handle client
    def handle(self, client, key):
        while True:
            try:
                json_message = client.recv(1024).decode(settings.code)
                encrypted_message = json_utils.decode_json(json_message)
                message = crypto.decrypt(encrypted_message, key)

                if message["title"] == "MESSAGE":
                    self.broadcast(json_message, client)
                elif message["title"] == "COMMAND":
                    self.command_analysis(message["text"], client)

            except Exception as error:

                print(error)

                self.remove_client(client)
                break

    # Receive clients message
    def receive(self):
        while True:
            client, addres = self.server.accept()
            print("Connected with " + str(addres))
            self.clients.append(client)

            # Requests key
            key = int(client.recv(1024).decode(settings.code))
            self.client_keys.append(key)

            # Requests nick
            self.send_message(json_utils.encode_system("NICK"), client)
            nick = client.recv(1024).decode(settings.code)
            self.nicknames.append(nick)



            try:
                print("{} join".format(nick))
            except:
                self.broadcast(("{}, pishi na angliyskom, byak".format(nick)))

            # Broadcast join
            self.broadcast(json_utils.encode_message("[{}] join to chat".format(nick)))

            # Start threading with client
            thread = threading.Thread(target=self.handle, args=(client, key, ))
            thread.start()

    def get_nickname_by_client(self, client):
        index = self.clients.index(client)
        return self.nicknames[index]

    def get_key_by_client(self, client):
        index = self.clients.index(client)
        return self.client_keys[index]

    # Analysis clients command
    def command_analysis(self, text, client):

        text = text.lower()
        command = text.split(" ")

        # Exit
        if (command[0] == "exit"):
            self.send_message((json_utils.encode_system("EXIT")), client)
            self.remove_client(client)
        elif command[0] == "status":
            status = "[Addres] {} \n [Name] {}".format(client.getpeername(), self.get_nickname_by_client(client))
            self.send_message(json_utils.encode_message(status), client)
        else:
            self.send_message((json_utils.encode_message("'{}' its not a command!!!".format(text))), client)



if __name__ == "__main__":
    chat = Chat(settings.server_host, settings.server_port)
    chat.start()
