import socket
import threading
import sys

import settings
import json_utils
import crypto

class Client:
    def __init__(self, port):
        self.nickname = input("How are you? ")
        self.key = crypto.cezar_generate_key()

        self.client = None

    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((settings.server_ip, settings.server_port))
        self.client.send(str(self.key).encode(settings.code))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    # Receive messages from another clients
    def receive(self):
        while True:

            encrypted_message = None
            encrypted_message = self.client.recv(1024).decode(settings.code)

            if encrypted_message:
                message_in_json = crypto.decrypt(encrypted_message, self.key)
                message = json_utils.decode_json(message_in_json)

                if message["title"] == "SYSTEM":
                    if message["text"] == "NICK":
                        self.client.send(self.nickname.encode(settings.code))  # Need
                    if message["text"] == "KEY":
                        self.client.send(self.key.encode(settings.code))  # Need
                    if message["text"] == "EXIT":
                        exit()

                elif message["title"] == "MESSAGE":
                    print(message["text"])
                else:
                    print(message)

    # Write message
    def write(self):
        while True:
            msg = input("")

            if msg != "":
                json_msg = self.message_to_json(msg)
                encrypted_msg = crypto.encrypt(json_msg, self.key)
                self.client.send(encrypted_msg.encode(settings.code))

    # Send message
    def send_message(self, msg):
        encrypted_message = crypto.encrypt(msg, self.key)

        self.client.send(encrypted_message.encode(settings.code))

    # Analysis message
    def message_to_json(self, text):

        # Command
        if text[0] == "/":
            text = text.replace("/", "")

            return json_utils.encode_command(text)

        # Just message
        else:
            return json_utils.encode_message("[{}] => {}".format(self.nickname, text))

    def exit(self):
        print("Goodbye!")
        sys.exit()

if __name__ == "__main__":
    client = Client(settings.client_port)
    client.start()







