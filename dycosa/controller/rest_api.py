#!/usr/bin/python3
import re
import json
from dycosa.drivers import Driver
from types import *
try:
    import usocket as socket
except:
    import socket


class RestApi:
    """
    This class is used to handle HTTP(S) requests
    """

    HTTP_200 = """HTTP/1.1 200 OK
Server: Dycosa (Python)
Content-Length: {length}
Content-Type: text/json; charset=iso-8859-1
Connection: Closed

{response}
"""

    HTTP_404 = """HTTP/1.1 404 Not Found
Server: Dycosa (Python)
Content-Length: 210
Content-Type: text/html; charset=iso-8859-1
Connection: Closed

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>

<head>
   <title>404 Not Found</title>
</head>

<body>
   <h1>Not Found</h1>
   <p>The requested URL was not found on this server.</p>
</body>

</html>
"""
                    
    def __init__(self, drivers):
        self.loadedDrivers = drivers

    def get_class_contet(self, value):
        result = dict()
        result['functions'] = list()
        for fnc in dir(value):
            if (not fnc.startswith("__") or fnc == "__name__"):  # Skip internal methods and properties
                fnc_value = getattr(value, fnc)
                if (type(fnc_value) == MethodType or type(fnc_value) == FunctionType):
                    result['functions'].append(fnc)
                else:
                    result[fnc.lstrip("_").rstrip("_")] = fnc_value
        return result

    def getcontent(self, uri):
        req = uri.rstrip('/').split('/')
        result = dict()
        value = self.loadedDrivers
        for i in range(2, len(req)):
            if(type(value) is dict):
                if(req[i] in value):
                    value = value[req[i]]
                else:
                    return None
            else:
                if(hasattr(value, req[i])):
                    value = getattr(value, req[i])
                else:
                    return None
        if value == self.loadedDrivers and len(req) == 2: #ToDo check API-Version
            for driver in self.loadedDrivers:
                result[driver] = self.get_class_contet(self.loadedDrivers[driver])
            return result
        if (isinstance(value, Driver)):
           result = self.get_class_contet(value)
        elif (type(value) == MethodType):
            result = value()
        elif (type(value) == FunctionType):
            print("Not implemented")
        else:
            result = None
        return result

    def run(self, ip="0.0.0.0"):
        request_pattern = "(GET|POST)?\ \/([\/\w*]*)\ (.*)\/(\.*.*)"
        request_regex = re.compile(request_pattern)
        s = socket.socket()

        # Binding to all interfaces - server will be accessible to other hosts!
        ai = socket.getaddrinfo(ip, 8080)
        addr = ai[0][-1]

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)
        print("REST-API: controller is running")

        while True:
            res = s.accept()
            client_sock = res[0]
            client_addr = res[1]
            print("REST-API: Handle request from", client_addr)

            client_stream = client_sock.makefile("rwb")

            req = client_stream.readline().decode('ascii')
            req = request_regex.search(req)
            url = req.groups()[1]
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n":
                    break
            content = self.getcontent(url)
            if(content is None):
                response = self.HTTP_404
            else:
                content = json.dumps(content)
                response = self.HTTP_200.format(length=len(content), response=content)
            client_stream.write(response.encode('ascii'))

            client_stream.close()
            client_sock.close()



