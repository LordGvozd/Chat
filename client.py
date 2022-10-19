import socket
import threading

import settings
import json_utils

class Client:
    def __init__(self, port):
        self.nickname = input("How are you? ")

        self.client = None

    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((settings.server_ip, settings.server_port))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    # Receive messages from another clients
    def receive(self):
        while True:
            try:
                message = None
                message_in_json = self.client.recv(1024).decode(settings.code)

                if(message_in_json):
                    message = json_utils.decode_json(message_in_json)
                    if (message["title"] == "SYSTEM"):
                        if(message["text"] == "NICK"):
                            self.client.send(self.nickname.encode(settings.code))
                    elif message["title"] == "MESSAGE":
                        print(message["text"])
                    else:
                        print(message)
            except Exception as error:
                print("Error 304: Egor join the chat")

    # Write message
    def write(self):
        while True:
            msg = "[{}] => {}".format(self.nickname, input(""))

            json_msg = json_utils.encode_message(msg)
            self.client.send(json_msg.encode(settings.code))


if __name__ == "__main__":
    client = Client(settings.client_port)
    client.start()







