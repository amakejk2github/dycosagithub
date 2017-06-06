#!/usr/bin/python3
import re
import json
from Drivers import Driver
from types import *
try:
    import usocket as socket
except:
    import socket


class RestApi:

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

        if (isinstance(value, Driver)):
            result['functions'] = list()
            for fnc in dir(value):
                if(not fnc.startswith("__")):  # Skip internal methods and propertys
                    fnc_value = getattr(value, fnc)
                    if(type(fnc_value) == MethodType or type(fnc_value) == FunctionType):
                        result['functions'].append(fnc)
                    else:
                        result[fnc] = fnc_value
        elif (type(value) == MethodType):
            result = value()
        elif (type(value) == FunctionType):
            print("Not implemented")
        else:
            result = None
        return result

    def run(self, micropython_optimize=False):
        request_pattern = "(GET|POST)?\ \/([\/\w*]*)\ (.*)\/(\.*.*)"
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
            url = req.groups()[1]
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n":
                    break
                print(h)
            content = self.getcontent(url)
            if(content is None):
                response = self.HTTP_404
            else:
                content = json.dumps(content)
                response = self.HTTP_200.format(length=len(content), response=content)
            client_stream.write(response.encode('ascii'))

            client_stream.close()
            if not micropython_optimize:
                client_sock.close()
            counter += 1
            print()



