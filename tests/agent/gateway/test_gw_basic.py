import os
from magic.utils.configloader import ConfigLoader


def test_default_config(gateway):

    gateway_root_path = os.path.dirname(
        os.path.realpath(__file__)) + '/../../../magic/gateway'

    config = ConfigLoader()
    config.load(
        default_config_path=gateway_root_path + '/default-config.hjson',
        user_config_path=gateway_root_path + '/user-config.hjson'
    )

    assert gateway.config == config
