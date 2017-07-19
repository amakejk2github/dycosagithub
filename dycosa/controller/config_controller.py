import json


class Config_Controller:
    """
    This class holds the Config File,
    and serves the information to other classes
    """

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
        with open('Node_config.json', 'w') as OutputFile:
            json.dump(self.config_data, OutputFile, indent=4, sort_keys=False)

    def set_config(self, attribute, entry, write_to_file):
        data = self.find_config_entry(attribute)
        settable_value = True
        if 'Settable' in data.keys():
            settable_value = data['Settable']
        if not settable_value:
            raise Exception(f"Attribute {attribute} is not settable")
        try:
            if 'Value' in data.keys():
                data["Value"] = entry
            else:
                data[attribute] = entry
        except:
            raise Exception (f"Fatal error occurred, while writing {attribute}")
        if write_to_file:
            self.write_config_to_data()