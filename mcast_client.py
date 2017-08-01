import socket, json

class mcast_client():

    def __init__(self, rest_endpoint):
        self.MCAST_Address = ('239.255.255.0', 1900)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rest_endpoint = rest_endpoint
        self.client.connect(self.MCAST_Address)

    def search(self, search_parameters, mcast_id):
        param = json.dumps(search_parameters)
        try:

            msg =('SEARCH '                                  + '\n\r' \
                + 'RESPONSE :' +  + str(self.rest_endpoint)  + '\n\r' \
                + 'MCAST-ID :' + str(mcast_id)               + '\n\r' \
                +                                              '\n\r' \
                + param

            msg = msg.encode('utf-8')

            self.client.send(msg)
        except Exception as e:
            print(e)


    def close():
        self.client.close()
        self = None

