from dycosa.drivers import *
from dycosa.controller.rest_api import RestApi
from dycosa.controller.multicast_sender import MulticastSender
from dycosa.controller.multicast_receiver import MulticastReceiver
# from dycosa.job.job_controller import JobController

import pprint
import json


class Controller:
    """
    This class is used to hold the following components of dycosa
    - The Webserver
    - The Job Controller
    - The Multicast receiver
    - The Multicast sender
    Also it loads the Drivers and serves them to the components
    """

    def __init__(self):
        self.config_data = self.load_config()
        self.drivers = self.load_drivers()
        self.multicast_sender = MulticastSender()
        self.multicast_receiver = MulticastReceiver()

    #       self.job_controller = JobController()

    def parse_config(self):
        pass

    def load_config(self):
        # Opens file and converts JSON object to strings, dicts, etc.
        with open('Node_Config.json', encoding='utf-8') as node_config:
            config_data = json.loads(node_config.read())
            return config_data

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
                            raise Exception("Driver {driver} does not implement the endpoint property".format(
                                driver=clsobj.__name__))
                        endpoint = clsobj.endpoint
                        i = 0
                        while (endpoint + str(i)) in drivers:
                            i = i + 1
                        drivers[endpoint + str(i)] = clsobj
                        print("Loaded driver of type {type} with endpoint {endpoint}".format(type=clsobj.__name__,
                                                                                             endpoint=endpoint + str(
                                                                                                 i)))
                except:
                    pass
        return drivers

    def run(self):
        api = RestApi(self.drivers)
        api.run()
