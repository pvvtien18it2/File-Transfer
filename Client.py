from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint
class Client(DatagramProtocol):
    def __init__(self, host, port):
        if host == 'localhost':
            host = "127.0.0.1"

        self.id = host, port
        self.address = None
        self.server = '127.0.0.1', 10000
        self.file = False
        print('Working on id: ', self.id)

    def startProtocol(self):
        self.transport.write('ready'.encode('utf-8'), self.server)


    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode('utf-8')

        if addr == self.server:
            print("Choose client from there\n", datagram)
            self.address = '127.0.0.1', int(input('Write port: '))
            reactor.callInThread(self.send_message)
        else:
            print(addr, ": ", datagram)

    def send_message(self):
        while True:
            # file = open('test.txt', 'r', encoding='utf-8').read(1024)
            file = open('image.jpg', 'rb', ).read(26214400)
            mgs = input().encode('utf-8').lstrip()
            if mgs != '' and len(mgs) == 0:
                self.save_file(file)
                # self.save_file(file.encode('utf-8'))
                mgs = 'Successfully!!!'
                self.transport.write(mgs.encode('utf-8'), self.address)
            else:
                self.transport.write(mgs, self.address)

    def save_file(self, file):
        file_save = open('test_save.jpg', 'wb')
        file_save.write(file)
        print()

if __name__ == "__main__":
    port = randint(1000, 5000)
    reactor.listenUDP(port, Client('localhost', port))
    reactor.run()

