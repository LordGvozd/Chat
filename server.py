import socket
import threading
import time

import json_utils
import settings


class Chat:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.server = None
        self.run = False

        self.clients = []
        self.nicknames = []

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

            self.clients.remove(client)
            client.close()

            nick = self.nicknames[index]
            self.nicknames.remove(nick)

            print("[{}] left the chat".format(nick))
            self.broadcast("[{}] left the chat".format(nick).encode(settings.code))

    # Sending message to all connected client
    def broadcast(self, msg, ignore_client="Not client, string"):
        for client in self.clients:
            try:
                if (client != ignore_client):
                    client.send(msg)
            except:
                self.remove_client(client)

    # Handle client
    def handle(self, client):
        while True:
            try:
                json_message = client.recv(1024)
                message = json_utils.decode_json(json_message)

                if message["title"] == "MESSAGE":
                    self.broadcast(json_message, client)
                elif message["title"] == "COMMAND":
                    self.command_analysis(message["text"], client)

            except:
                self.remove_client(client)
                break

    # Receive clients message
    def receive(self):
        while True:
            client, addres = self.server.accept()
            print("Connected with " + str(addres))

            # Requests nick
            client.send(json_utils.encode_system("NICK").encode(settings.code))
            nick = client.recv(1024).decode(settings.code)
            self.nicknames.append(nick)
            self.clients.append(client)

            try:
                print("{} join".format(nick))
            except:
                self.broadcast(("{}, pishi na angliyskom, byak".format(nick)).encode(settings.code))

            # Broadcast join
            self.broadcast(json_utils.encode_message("[{}] join to chat".format(nick)).encode(settings.code))

            # Start threading with client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def get_nickname_by_client(self, client):
        index = self.clients.index(client)
        return self.nicknames[index]
    # Analysis clients command
    def command_analysis(self, text, client):

        text = text.lower()
        command = text.split(" ")

        # Exit
        if(command[0] == "exit"):
            client.send((json_utils.encode_system("EXIT")).encode(settings.code))
            self.remove_client(client)
        elif command[0] == "status":
            status = "[Addres] {} \n [Name] {}".format(client.getpeername(), self.get_nickname_by_client(client))
            client.send(json_utils.encode_message(status).encode(settings.code))
        else:
            client.send((json_utils.encode_message("'{}' its not a command!!!".format(text))).encode(settings.code))



if __name__ == "__main__":
    chat = Chat(settings.server_host, settings.server_port)
    chat.start()
