<<<<<<< HEAD
from magic.configloader import ConfigLoader
import os


def test_default_config(gateway):

	gateway_root_path = os.path.dirname(os.path.realpath(__file__)) + '/../../magic/gateway'

	config = ConfigLoader()
	config.load(
        default_config_path=gateway_root_path + '/default-config.hjson',
        user_config_path=gateway_root_path + '/user-config.hjson'
    )

=======
from magic.gateway.config.configloader import ConfigLoader

def test_default_config(gateway):
	config = ConfigLoader()
	config.load()
>>>>>>> master
	assert gateway.config == config
