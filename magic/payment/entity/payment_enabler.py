from web3 import Web3

class PaymentEnabler():

    def __init__(self, web3, token_contract, config):

        self.addr = Web3.toChecksumAddress(config['admin']['eth_address'])
        self.key = config['admin']['eth_private_key']
        self.airdrop_eth = config['admin']['airdrop_eth']
        self.airdrop_mgc = config['admin']['airdrop_mgc']
        self.web3 = web3
        self.nonce = web3.eth.getTransactionCount(self.addr)
        self.token_contract = token_contract

    def refresh_nonce(self):
        self.nonce = self.web3.eth.getTransactionCount(self.addr)
        return self.nonce

    def next_nonce(self):
        self.nonce += 1
        return self.nonce

    def send_tx(self, tx):

        signed_tx = self.web3.eth.account.signTransaction(tx, private_key=self.key)
        receipt = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return receipt

    async def airdrop(self, receiver_addr):

        receiver_addr = Web3.toChecksumAddress(receiver_addr)

        # Transfer tokens first.
        token_transfer_tx = self.token_contract.functions.transfer(receiver_addr, self.airdrop_mgc).buildTransaction({
            'chainId': 4,   # Rinkeby for now.
            'gas': 70000,
            'gasPrice': Web3.toWei('1', 'gwei'),
            'nonce': self.refresh_nonce()
        })

        token_receipt = self.send_tx(token_transfer_tx)

        # Transfer a bit of ether for the approve call (before we make it delegated)
        eth_transfer_tx = {
            'chainId': 4,   # Rinkeby for now.
            'gas': 70000,
            'gasPrice': Web3.toWei('1', 'gwei'),
            'nonce': self.next_nonce(),
            'value': self.airdrop_eth,
            'to': receiver_addr
        }

        eth_receipt = self.send_tx(eth_transfer_tx)

        return (token_receipt, eth_receipt)