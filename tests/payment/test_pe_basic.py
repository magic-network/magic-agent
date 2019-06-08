from magic.configloader import ConfigLoader
import os


def test_default_config(payment_enabler):

    payment_root_path = os.path.dirname(
        os.path.realpath(__file__)) + '/../../magic/payment'

    config = ConfigLoader()
    config.load(
        default_config_path=payment_root_path + '/default-config.hjson',
        user_config_path=payment_root_path + '/user-config.hjson'
    )

    assert payment_enabler.config == config
