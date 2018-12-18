from ethereum.utils import privtoaddr, encode_hex, ecsign, sha3, normalize_key, ecrecover_to_pub
# from web3.auto import w3
from web3 import Web3

# Generate a new ethereum account
def generate_account():
    account = Web3.eth.account.create()

    return type('obj', (object,), {
        'pubkey': account.address,
        'privkey': encode_hex(account.privateKey)
    })

def add_hex_prefix(hex):
    return '0x' + hex

def get_pub_from_privkey(private_key):
    return encode_hex(privtoaddr(private_key))

def recover(message, v, r, s):

    message_hash = sha3(message)
    recovered_blob = ecrecover_to_pub(message_hash, int(v), int(r), int(s))
    pub_account = encode_hex(sha3(recovered_blob)[-20:])

    return pub_account

def sign(message, private_key):

    # keccak256 the agreed upon message.
    message_hash = sha3(message)

    # convert private key to binary
    priv_key = normalize_key(private_key)

    # sign with private key
    signature = ecsign(message_hash, priv_key)

    # stringify signature for transport
    stringified_sig = '-'.join(str(x) for x in signature)

    return stringified_sig

def parse_address(address_string):
    return Web3.toChecksumAddress(address_string.lower())