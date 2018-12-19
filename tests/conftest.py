import pytest
from magic.payment.app import MagicPayment
from magic.gateway.app import MagicGateway


@pytest.fixture(scope='session', autouse=True)
def gateway():
    gateway = MagicGateway()
    return gateway

@pytest.fixture(scope='session', autouse=True)
def payment_enabler():
    payment_enabler = MagicPayment()
    return payment_enabler