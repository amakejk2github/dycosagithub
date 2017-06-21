#!/usr/bin/python3
from dycosa.drivers import *
from dycosa.controller.rest_api import RestApi


class Controller:
    """
    This class is used to hold the following components of dycosa
    - The webserver
    - The JobRunner
    - The Multicast receiver
    - The Multicast sender
    Also it loads the Drivers and serves them to the components
    """
    def __init__(self):
        self.drivers = self.load_drivers()

    def load_drivers(self):
        drivers = dict()
        global_objs = list(globals().items())
        for name, obj in global_objs:
            for subObj in dir(obj):

                cls = getattr(obj, subObj)
                try:
                    if (cls is not Driver and issubclass(cls, Driver)):
                        clsobj = cls()
                        if not hasattr(clsobj, "endpoint"):
                            raise Exception("Driver {driver} does not implment the endpoint property".format(driver = clsobj.__name__))
                        endpoint = clsobj.endpoint
                        i = 0
                        while (endpoint + str(i)) in drivers:
                            i = i + 1
                        drivers[endpoint + str(i)] = clsobj
                        print("Loaded driver of type {type} with endpoint {endpoint}".format(type = clsobj.__name__, endpoint = endpoint + str(i)))
                except:
                    pass
        return drivers

    def run(self):
        api = RestApi(self.drivers)
        api.run()


