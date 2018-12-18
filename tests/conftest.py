import pytest
<<<<<<< HEAD
from magic.gateway.app import MagicGateway
=======
from magic.gateway.magic import MagicGateway
>>>>>>> master

@pytest.fixture(scope='session', autouse=True)
def gateway():
    gateway = MagicGateway()
    return gateway
