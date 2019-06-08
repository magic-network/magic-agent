import pytest
from magic.payment.agent import MagicPayment
from magic.gateway.agent import MagicGateway


@pytest.fixture(scope='session', autouse=True)
def gateway():
    return MagicGateway()


@pytest.fixture(scope='session', autouse=True)
def payment_enabler():
    return MagicPayment()
