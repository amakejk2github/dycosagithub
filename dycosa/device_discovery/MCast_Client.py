import socket, json

class MCast_Client():

    def __init__(self, rest_API, rest_endpoint):
        self.MCAST_Adress = ('239.255.255.0', 1900)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rest_API = rest_API
        self.rest_endpoint = rest_endpoint
        self.client.connect(('239.255.255.0', 1900))

    def search(self, search_parameters ):
        param = json.dumps(search_parameters)
        try:

            msg = ('SEARCH '   + self.rest_endpoint)    + '\n\r' \
                + 'RESPONSE' + str(self.rest_API)      + '\n\r' \
                +                                        '\n\r' \
                + param

            msg = msg.encode('utf-8')
            self.client.send(msg)
        except Exception as e:
            print(e)

    def close():
        self.client.close()
        self = None

