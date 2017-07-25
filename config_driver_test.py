from dycosa.drivers.config_driver import Config_Driver
import pytest
import json

@pytest.fixture()
def prefab():
    return Config_Driver()

def test_get_function(prefab):
    with open('Node_Config.json', encoding='utf-8') as node_config:
        config_data = json.loads(node_config.read())
    assert prefab.get_config() == config_data

def test_set_function(prefab):
    prefab.set_config(["Device", "Sleep"], 0)
    with open('Node_Config.json', encoding='utf-8') as node_config:
        config_data = json.loads(node_config.read())
    assert prefab.get_config() == config_data

def test_set_function2(prefab):
    with pytest.raises(Exception):
        prefab.set_config(["Device", "Location", "M_Value", "Text"], "P7.2.03")


