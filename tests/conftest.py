import pytest
from magic.gateway.app import MagicGateway


@pytest.fixture(scope='session', autouse=True)
def gateway():
    gateway = MagicGateway()
    return gateway
