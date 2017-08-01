import socket, json

class mcast_server():

    def __init__(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(('0.0.0.0', 1900))
        self.listener.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton('239.255.255.0') + socket.inet_aton('0.0.0.0'))

    def listen(self):
        self.running = True
        while self.running:
            (data, addr) = self.listener.recvfrom(1024)
            if data.startswith(b'SEARCH'):
                print('Suchanfrage angekommen\r' + str(data, 'utf-8'))
                header, body = data.split('\r\n\r\n',1)
                commands = header.split('\r\n')
                for command in commands:
                    try:
                        field, content = command.split(': ', 1)
                        if field == "MCastID":
                            mcast_id = content
                        if field == "Response":
                            response = content
                    except Exception:
                        pass
                    self_config = {} #get_config()
                    drivers = mcast_search_drivers(self_config, json.load(body))
                    #response drivers to external RestAPI
            else:
                print('andere Anfrage')

    def stop(self):
        self.running = False
        self.listener.close()




def _mcast_compare_config(self_config, searched_config):
    try:
        if(self_config['visible'] == False):
            print('Nicht visible')
            return False
    except Exception as e:
        pass

    fitting = True
    for index in searched_config:
        try:
            self_index = self_config[index]
        except Exception as e:
            print('Gab den Index nicht')
            return False

        if (type(self_index) == dict):
            fitting = fitting & _mcast_compare_config(self_index, searched_config[index])
        else:
            fitting = fitting & (self_index == searched_config[index])
            print('Falscher Eintrag')
        if (fitting == False):
            break

    return fitting


def _mcast_search_drivers(self_config, search_config):
    fitting = True
    try:
        fitting = _mcast_compare_config(self_config['device'], search_config['device'])
    except Exception:
        pass

    if fitting == False:
        return None

    try:
        fitting = _mcast_compare_config(self_config['network'], search_config['network'])
    except Exception:
        pass

    if fitting == False:
        return None
    try:
        drivers = search_config['drivers']
    except:
        return None

    try:
        for key in drivers.keys():
            if key == 'any':
                for self_driver in self_config['drivers']:
                    if _mcast_compare_config(self_driver,drivers['any']):
                        return self_driver
            else:
                try:
                    _mcast_compare_config(self_config['drivers'][key], drivers[key])
                    return drivers[key]
                except Exception:
                    pass
    except Exception as e:
        print(e)
    return None

