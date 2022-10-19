import socket
import threading

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

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message, client)
            except:
                self.remove_client(client)
                break

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


if __name__ == "__main__":
    chat = Chat(settings.server_host, settings.server_port)
    chat.start()
