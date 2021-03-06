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
        self.config_data = self._load_config()


    def _load_config(self):
        # Opens file and converts JSON object to strings, dicts, etc.
        with open('Node_Config.json', encoding='utf-8') as node_config:
            config_data = json.loads(node_config.read())
            return config_data

    def _write_config_to_data(self):
        try:
            with open('Node_config.json', 'w') as OutputFile:
                json.dump(self.config_data, OutputFile, indent=4, sort_keys=False)
        except:
            raise Exception("Write to config file failed")

    def get_config(self):
        return self.config_data

    def set_config(self, list, entry):
        if entry == '':
            raise Exception("Cannot write empty entry")
        data = self.config_data
        attribute_name = ""
        m_value_found = False
        settable_value = True
        for key in list:
            if key == 'Settable' or key == 'Visible':
                raise Exception("Access to attribute {key_name} is restricted".format(key_name=key))
            if key in data.keys():
                if not m_value_found:
                    data = data[key]
                if key == 'M_Value':
                    m_value_found = True
                try:
                    if 'Settable' in data.keys():
                        if not data['Settable']:
                            settable_value = False
                except:
                    pass
                attribute_name = key
            else:
                raise Exception("Key {input} is not in the config".format(input=key))
        if not settable_value:
            raise Exception("Attribute {output} is not settable".format(output=attribute_name))
        if 'Value' in data.keys():
            data["Value"] = entry
        else:
            data[key] = entry
        self._write_config_to_data()
