from dycosa.drivers import *
from dycosa.controller.rest_api import RestApi
from dycosa.controller.multicast_sender import MulticastSender
from dycosa.controller.multicast_receiver import MulticastReceiver
from dycosa.drivers.config_driver import Config_Driver
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
        self.config = Config_Driver()
        self.drivers = self.load_driver_from_config()
        self.multicast_sender = MulticastSender()
        self.multicast_receiver = MulticastReceiver()
        #self.job_controller = JobController()


    def load_driver_from_config(self):
        global_objs = list(globals().items())
        drivers = dict()
        loadable_drivers = dict()
        for name, object in global_objs:
            for subObj in dir(object):
                cls = getattr(object, subObj)
                try:
                    if(cls is not Driver and issubclass(cls, Driver)):
                        loadable_drivers[name] = cls
                except:
                    pass
        data = self.config.get_config()
        data = data["Drivers"]
        for key in data.keys():
            driver_data = data[key]
            class_name = driver_data["InstanceOf"]
            if not class_name in loadable_drivers.keys():
                raise Exception ("Driver {name} is not implemented or wrong name given".format(name = class_name))
            classobj = loadable_drivers[class_name]()
            #TODO implement drivers to accept comments and internal configs as parameters, then loadable_drivers[class_name](driver_data["Comment], driver_data["Config"])
            if not hasattr(classobj, "endpoint"):
                raise Exception("Driver {name} does not implement the endpoint property".format(name=classobj.__name__))
            endpoint = classobj.endpoint
            i = 0
            while (endpoint + str(i)) in drivers:
                i = i + 1
            drivers[endpoint + str(i)] = classobj
            print("Loaded driver of type {name} with endpoint {end}".format(name=classobj.__name__, end=endpoint + str(i)))
        return drivers






    def run(self):
        api = RestApi(self.drivers)
        api.run()