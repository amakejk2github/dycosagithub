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
        self.config_path_dict = dict()
        self.create_dict_for_config(self.config_data, "root", "")
        self.drivers = self.load_drivers()
        self.multicast_sender = MulticastSender()
        self.multicast_receiver = MulticastReceiver()
        print(self.get_config("Type"))  # Test function
        print(self.get_config("Sleep"))  # Test function
        print(self.get_config("Text"))  # Test function
        print(self.get_config("Permanent_power"))  # Test function

    #       self.job_controller = JobController()

    def load_config(self):
        # Opens file and converts JSON object to strings, dicts, etc.
        with open('Node_Config.json', encoding='utf-8') as node_config:
            config_data = json.loads(node_config.read())
            return config_data

    def create_dict_for_config(self, JSON_data, path, last_key):
        try:
            for key, value in JSON_data.items():
                if key == 'Value':
                    self.config_path_dict[last_key] = path
                if key != 'Settable' and key != 'Visible' and key != 'Value':
                    self.create_dict_for_config(JSON_data[key], path + "/" + key, key)
        except:
            self.config_path_dict[last_key] = path

    def get_config(self, attribute):
        data = self.find_config_entry(attribute)
        visible_value = True
        try:
            visible_value = data['Visible']
        except:
            pass
        if visible_value:
            try:
                return data['Value']
            except:
                return data
        else:
            raise Exception(f"Attribute {attribute} is not visible")

    def set_config(self, attribute, entry):
        data = self.find_config_entry(attribute)
        settable_value = True
        try:
            settable_value = data['Settable']
        except:
            pass



    def find_config_entry(self, attribute):
        try:
            path = self.config_path_dict[attribute]
        except:
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
