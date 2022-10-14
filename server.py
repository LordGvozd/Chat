import socket, time

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.clients = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))
        
        self.run = False

        print("Server init")

    def start(self):
        self.run = True
        print("Server started")
        #self.server.listen(10)
        while self.run:


            data, addr = self.server.recvfrom(1024)
            
            nowtime = 'durak'
            
            print("["+addr[0]+"]=["+nowtime+"]")
            print(data.decode("utf-8"))


            if (addr not in self.clients):
                self.clients.append(addr)



            for client in self.clients:
                if (addr !=addr[0]):
                    self.server.sendto(data, client)


        server.close()





    


if __name__ == "__main__":
    server = Server("0.0.0.0", 7878)
    server.start()
