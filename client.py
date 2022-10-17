import socket
import threading

import settings

class Client:
    def __init__(self, port):
        self.nickname = "Man"

        self.client = None



    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((settings.server_ip, settings.server_port))

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode(settings.code)
                if (message == "NICK"):
                    self.client.send(self.nick().encode(settings.code))
                else:
                    print(message)
            except:
                print("Error 304: Egor kill you")

    def write(self):
        while True:
            msg = "[{}] => {}".format(self.nickname, input(""))
            self.client.send(msg.encode(settings.code))

    def nick(self):

        self.nickname = input("First say you name: ")
        return self.nick


if __name__ == "__main__":
    client = Client(settings.client_port)
    client.start()







