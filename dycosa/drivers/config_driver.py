from dycosa.drivers import Driver

import json


class Config_Driver(Driver):
    """
    This class holds the Config File,
    and serves the information to other classes

    """

    __name__ = "Config_Driver"
    endpoint = "Config"

    def __init__(self):
        self.config_data = self.load_config()

    def load_config(self):
        # Opens file and converts JSON object to strings, dicts, etc.
        with open('Node_Config.json', encoding='utf-8') as node_config:
            config_data = json.loads(node_config.read())
            return config_data

    def get_config(self):
        return self.config_data

    def write_config_to_data(self):
        try:
            with open('Node_config.json', 'w') as OutputFile:
                json.dump(self.config_data, OutputFile, indent=4, sort_keys=False)
        except:
            raise Exception("Write to config file failed")

    def set_config(self, list, entry):
        data = self.config_data
        attribute_name = ""
        settable_value = True
        for key in list:
            if key in data.keys():
                data = data[key]
                if 'Settable' in data.keys():
                    if not data['Settable']:
                        settable_value = False
                attribute_name = key
            else:
                raise Exception("Key {input} is not in the config".format(input=key))
        if attribute_name == 'Settable' or attribute_name == 'Visible':
            raise Exception("Access to attribute {key_name} is restricted".format(key_name = attribute_name))
        if not settable_value:
            raise Exception("Attribute {output} is not settable".format(output=attribute_name))
        try:
            if 'Value' in data.keys():
                data["Value"] = entry
            else:
                data[attribute_name] = entry
        except:
            raise Exception("Fatal error occurred, while writing {output}".format(output=attribute_name))
        self.write_config_to_data()
