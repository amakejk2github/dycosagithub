#!/usr/bin/python3
import re
import json
import asyncio
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
    CONTENT_TYPE_HTML = "text/html"
    CONTENT_TYPE_JSON = "text/json"
    RESPONSE_HEADERS = """HTTP/1.1 {status}
Server: Dycosa (Python)
Content-Length: {length}
Content-Type: {content_type}; charset=iso-8859-1
Connection: Closed

{response}
"""
    HTTP_200 = "200 OK"
    HTTP_404 = "404 Not Found"
    HTTP_404_RESPONSE = """
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

    HTTP_500 = "500 Internal Server Error"
    HTTP_500_RESPONSE = """
    <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
    <html>

    <head>
       <title>Internal Server Error</title>
    </head>

    <body>
       <h1>Internal Server Error</h1>
       <h2>Additonal infos:</h2>
       <p>{infos}</p>
    </body>

    </html>
    """
                    
    def __init__(self, drivers):
        self.loadedDrivers = drivers

    def get_class_contet(self, value):
        result = dict()
        result['functions'] = list()
        for fnc in dir(value):
            if (not fnc.startswith("__") or fnc == "__name__"):  # Skip internal methods and propertys
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

    @asyncio.coroutine
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
            yield from asyncio.sleep(1)
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
            try:
                content = self.getcontent(url)
                if(content is None):
                    response = self.RESPONSE_HEADERS.format(status=self.HTTP_404, length=len(self.HTTP_404_RESPONSE), response=self.HTTP_404_RESPONSE, content_type=self.CONTENT_TYPE_HTML)
                else:
                    content = json.dumps(content)
                    response = self.RESPONSE_HEADERS.format(status=self.HTTP_200,length=len(content), response=content, content_type=self.CONTENT_TYPE_JSON)
            except Exception as e:
                response = self.HTTP_500_RESPONSE.format(str(e))
                response = self.RESPONSE_HEADERS.format(status=self.HTTP_500,length=len(response),response=response, content_type=self.CONTENT_TYPE_HTML)
            client_stream.write(response.encode('ascii'))


            client_stream.close()
            client_sock.close()



