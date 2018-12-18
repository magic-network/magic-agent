from magic.gateway.config.configloader import ConfigLoader

def test_default_config(gateway):
	config = ConfigLoader()
	config.load()
	assert gateway.config == config
