#!/usr/bin/python3
from Drivers import *
import re
import json
#from types import ModuleType, ClassType
try:
    import usocket as socket
except:
    import socket

class RestApi:
    loadedDrivers = dict()

    CONTENT = b"""\
    HTTP/1.0 200 OK

    Hello #%d from MicroPython!"""

    def loadDrivers(self):
        drivers = dict()
        global_objs = list(globals().items())
        for name, obj in global_objs:
            for subObj in dir(obj):
                cls = getattr(obj, subObj)
                if(cls is not Driver and isinstance(cls, type) and issubclass(cls, Driver)):
                    clsObj = cls()
                    self.loadedDrivers[clsObj.__name__] = clsObj
                    
    def __init__(self):
        self.loadDrivers()

    def run(self, micropython_optimize=False):
        request_pattern = "(GET|POST)?\ ([\/\w*]*)\ (.*)\/(\.*.*)"
        request_regex = re.compile(request_pattern)
        s = socket.socket()

        # Binding to all interfaces - server will be accessible to other hosts!
        ai = socket.getaddrinfo("0.0.0.0", 8080)
        print("Bind address info:", ai)
        addr = ai[0][-1]

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)
        print("Listening, connect your browser to http://<this_host>:8080/")

        counter = 0
        while True:
            res = s.accept()
            client_sock = res[0]
            client_addr = res[1]
            print("Client address:", client_addr)
            print("Client socket:", client_sock)

            if not micropython_optimize:
                # To read line-oriented protocol (like HTTP) from a socket (and
                # avoid short read problem), it must be wrapped in a stream (aka
                # file-like) object. That's how you do it in CPython:
                client_stream = client_sock.makefile("rwb")
            else:
                # .. but MicroPython socket objects support stream interface
                # directly, so calling .makefile() method is not required. If
                # you develop application which will run only on MicroPython,
                # especially on a resource-constrained embedded device, you
                # may take this shortcut to save resources.
                client_stream = client_sock

            print("Request:")
            req = client_stream.readline().decode('ascii')
            req = request_regex.search(req)
            url = req.groups()[1].split('/')
            print(req.groups())
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n":
                    break
                print(h)
            if(len(url) == 4):
                links = list()
                for link in dir(self.loadedDrivers[url[3]]):
                    if not link.startswith('__'):
                        links.append(link)
                result = dict()
                result['links'] = links
            else:
                result = getattr(self.loadedDrivers[url[3]], url[4])()
            client_stream.write(json.dumps(result).encode('ascii'))

            client_stream.close()
            if not micropython_optimize:
                client_sock.close()
            counter += 1
            print()


if __name__ == "__main__":
    api = RestApi()
    api.run()
