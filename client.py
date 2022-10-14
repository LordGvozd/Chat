import socket, threading, time

class Client():
    def __init__(self, host, port, key=1111):
        self.host = host
        self.port = port
        self.key = key

        self.shutdown = False
        self.join = False

    def receving(self,name, sock):
        
        while not  self.shutdown:
            while True:
                data, addr = sock.recvfrom(1024)
                print(data.decode("utf-8"))
    def run(self, server_ip):
        server = ("94.228.112.236", 7878)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, 0))
        #s.setblocking(0)

        name = input("Name: ")

        rT = threading.Thread(target = self.receving, args = ("RecvThread", s))
        rT.start()

        while self.shutdown == False:
            if (self.join == False):
                s.sendto((("["+name+"] join chat")).encode("utf-8"), server)
                self.join = True
            else:
                try:
                    message = input(": ")
                    if(message != ""):
                        s.sendto((("["+name+"] => "+message)).encode("utf-8"), server)

                        time.sleep(0.2)
                except:
                    print("Byka error - you debil")
        rT.join()
        s.close()






if __name__ =="__main__":
    client = Client(socket.gethostbyname(socket.gethostname()), 8787)
    client.run(socket.gethostbyname(socket.gethostname()))




