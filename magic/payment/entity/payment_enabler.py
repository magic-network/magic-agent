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
        """Syncs our internal nonce with a nonce generated based upon transaction count.

        Returns:
            The snyced nonce number

        """
        self.nonce = self.web3.eth.getTransactionCount(self.addr)
        return self.nonce

    def next_nonce(self):
        """Increases our internal nonce.  Required when you have two transactions to be submitted in likely in the
        same block due to them being submitted at the same time.

        Returns:
            The increase nonce number.

        """
        self.nonce += 1
        return self.nonce

    def send_tx(self, tx):
        """Utility method to sign and send a raw transaction using the payment enablers private key.

        Returns:
            Eth receipt id

        """

        signed_tx = self.web3.eth.account.signTransaction(tx, private_key=self.key)
        receipt = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        return receipt

    async def airdrop(self, receiver_addr):
        """Sends ethereum and MGC tokens to the receiver_addr account.

        Args:
            receiver_addr: the user to whom the airdrop assets should be sent.
s
        Returns:
            Tuple of (token tx receipt, eth tx receipt)

        """

        receiver_addr = Web3.toChecksumAddress(receiver_addr)

        # Transfer tokens first.
        token_transfer_tx = self.token_contract.functions.transfer(receiver_addr, self.airdrop_mgc).buildTransaction({
            'chainId': 4,   # TODO: Make this a config setting.  Rinkeby for now.
            'gas': 70000,   # Needs to be dynamically determined?
            'gasPrice': Web3.toWei('1', 'gwei'),
            'nonce': self.refresh_nonce()
        })

        token_receipt = self.send_tx(token_transfer_tx)

        # Transfer a bit of ether for the approve call (before we make it delegated)
        eth_transfer_tx = {
            'chainId': 4,   # TODO: Make this a config setting.  Rinkeby for now.
            'gas': 70000,   # Needs to be dynamically determined?
            'gasPrice': Web3.toWei('1', 'gwei'),
            'nonce': self.next_nonce(),
            'value': self.airdrop_eth,
            'to': receiver_addr
        }

        eth_receipt = self.send_tx(eth_transfer_tx)

        return (token_receipt, eth_receipt)