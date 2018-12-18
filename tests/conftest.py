import pytest
from magic.gateway.magic import MagicGateway

@pytest.fixture(scope='session', autouse=True)
def gateway():
    gateway = MagicGateway()
    return gateway
