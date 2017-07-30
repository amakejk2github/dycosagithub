from dycosa.drivers import *
from dycosa.controller.rest_api import RestApi
from dycosa.job.job_controller import JobController
import asyncio
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
        job_controller = JobController()
        self.drivers['jobs'] = job_controller
        #config_controller = ConfigController()
        #self.drivers['config'] = configController
        #mcast_controller = McastController()
        api = RestApi(self.drivers)
        loop = asyncio.get_event_loop()
        #tasks = (
        #    job_controller.run(),
        #    api.run()
        #    mcast_controller.run()
        #)
        loop.run_until_complete(asyncio.gather(
            job_controller.run(),
            api.run()       #TODO fix bug, when both are in loop none of them is really executed, if standing alone everything works
        ))
        loop.close()


