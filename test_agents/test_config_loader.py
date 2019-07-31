import os
from magic.utils.configloader import ConfigLoader

def test_default_config():

    root_path = os.path.dirname(os.path.realpath(__file__))

    config = ConfigLoader()
    config.load(default_config_path=root_path + '/default-config.hjson')

    assert config["key"] == "value"
    assert config["nest"]["nest_key_1"] == 1
    assert config["nest"]["nest_key_2"] == "abc"
    assert config["nest"]["nest_key_3"] == [1, 2, 3]

def test_user_config():

    root_path = os.path.dirname(os.path.realpath(__file__))

    config = ConfigLoader()
    config.load(default_config_path=root_path + '/default-config.hjson',
        user_config_path=root_path + '/user-config.hjson')

    assert config["key"] == "new_value"
    assert config["nest"]["nest_key_1"] == 2
    assert config["nest"]["nest_key_2"] == "abc"
    assert config["nest"]["nest_key_3"] == [4, 5, 6]

def test_env_config():

    os.environ["KEY"] = "env_value"
    os.environ["NEST_NEST_KEY_3"] = "[7, 8, 9]"

    root_path = os.path.dirname(os.path.realpath(__file__))

    config = ConfigLoader()
    config.load(default_config_path=root_path + '/default-config.hjson',
        user_config_path=root_path + '/user-config.hjson')

    assert config["key"] == "env_value"
    assert config["nest"]["nest_key_1"] == 2
    assert config["nest"]["nest_key_2"] == "abc"
    assert config["nest"]["nest_key_3"] == [7, 8, 9]