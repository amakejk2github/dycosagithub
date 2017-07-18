import socket, json

class MCast_Server():

    def __init__(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(('0.0.0.0', 1900))
        self.listener.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton('239.255.255.0') + socket.inet_aton('0.0.0.0'))

    def listen(self):
        self.running = True
        while self.running:
            (data, addr) = self.listener.recvfrom(1024)
            if data.startswith(b'SEARCH'):
                print('Suchanfrage angekommen')
            else:
                print('andere Anfrage')

    def stop(self):
        self.running = False
