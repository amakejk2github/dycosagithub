from dycosa.drivers import *
from dycosa.controller.rest_api import RestApi
from dycosa.controller.multicast_sender import MulticastSender
from dycosa.controller.multicast_receiver import MulticastReceiver
# from dycosa.job.job_controller import JobController

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
        self.drivers = self.load_drivers()
        self.multicast_sender = MulticastSender()
        self.multicast_receiver = MulticastReceiver()
        #self.job_controller = JobController()





    def find_config_entry(self, attribute):
        if attribute in self.config_path_dict.keys():
            path = self.config_path_dict[attribute]
        else:
            raise Exception(f"Attribute {attribute} is not available")
        list_of_path = path.split('/')
        data = self.config_data
        for pathpart in list_of_path:
            if pathpart != "root":
                data = data[pathpart]
        return data

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
                            raise Exception(f"Driver {clsobj.__name__} does not implement the endpoint property")
                        endpoint = clsobj.endpoint
                        i = 0
                        while (endpoint + str(i)) in drivers:
                            i = i + 1
                        drivers[endpoint + str(i)] = clsobj
                        print(f"Loaded driver of type {clsobj.__name__} with endpoint {endpoint + str(i)}")
                except:
                    pass
        return drivers

    def run(self):
        api = RestApi(self.drivers)
        api.run()
