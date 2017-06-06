#!/usr/bin/python3
from Drivers import *
from RestApi import RestApi


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
                if (cls is not Driver and isinstance(cls, type) and issubclass(cls, Driver)):
                    clsobj = cls()
                    drivers[clsobj.__name__] = clsobj
        return drivers

    def run(self):
        api = RestApi(self.drivers)
        api.run()

if __name__ == "__main__":
    con = Controller()
    con.run()



