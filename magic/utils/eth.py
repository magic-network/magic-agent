import os
from ethereum.utils import sha3
from web3 import Web3
from web3.auto import w3

# Generate a new ethereum account


def generate_account():

    acct = w3.eth.account.create(os.urandom(4096))
    priv = acct.privateKey
    address = acct.address
    priv_hex = priv.hex()

    return type('obj', (object,), {
        'address': address,
        'privkey': priv_hex,
    })


def verify_sig(message, signature, address):
    msg_hash = sha3(message)
    recovered_address = w3.eth.account.recoverHash(
        msg_hash, signature=signature)
    return address == recovered_address


def parse_address(address_string):
    return Web3.toChecksumAddress(address_string.lower())
