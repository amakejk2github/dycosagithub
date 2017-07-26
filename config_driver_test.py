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

@pytest.mark.parametrize("input_list, input_entry, output" , [
    (["Device", "Location", "M_Value", "Text"], "P7.2.03" , "Attribute Text is not settable"),
    (["Device", "Sleep", "Visible"], False, "Access to attribute Visible is restricted"),
    (["Device", "Batterie"], "Off", "Key Batterie is not in the config"),
    (["Device", "Sleep"], "", "Cannot write empty entry")
])

def test_set_function2(prefab, input_list, input_entry, output):
    try:
        prefab.set_config(input_list, input_entry)
    except Exception as e:
        assert str(e) == output



