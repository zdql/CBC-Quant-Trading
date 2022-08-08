from eth_utils import address
from web3 import Web3
import os
from solc import compile_standard, install_solc
from dotenv import load_dotenv
import json


load_dotenv()


class Deployer:

    def __init__(self, RPCURL, CHAINID, ADDRESS, CONTRACT_NAME):
        self._RPCURL = RPCURL
        self._CHAINID = CHAINID
        self._ADDRESS = ADDRESS
        self._PRIVATE_KEY = os.getenv('PRIVATE_KEY')
        self._CONTRACT_NAME = CONTRACT_NAME

    def compile(self, version):
        name = self._CONTRACT_NAME
        with open(f"./{name}.sol", "r") as file:
            simple_storage_file = file.read()

        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"Trader.sol": {"content": simple_storage_file}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                        }
                    }
                },
            },
            solc_version=version,
        )

        with open(f"compiled_{name}.json", "w") as file:
            json.dump(compiled_sol, file)

          # get bytecode
        self._bytecode = compiled_sol["contracts"][f"{name}.sol"]["Trader"]["evm"]["bytecode"]["object"]

        # get abi
        self._abi = json.loads(
            compiled_sol["contracts"][f"{name}.sol"]["Trader"]["metadata"]
        )["output"]["abi"]

    def sign(self, provider, transaction):
        signed_tx = provider.eth.account.signTransaction(
            transaction, private_key=self._PRIVATE_KEY,)
        return signed_tx

    def send(self, provider, signed_tx):
        tx_hash = provider.eth.account.send_raw_transaction(
            signed_tx.rawTransaction)
        tx_receipt = provider.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def deploy_Trader(self, router, token0, token1, fee):

        # set up connection
        w3 = Web3(Web3.WebsocketProvider(self._RPCURL))

        self.compile()

        # initialize contract
        Trader = w3.eth.contract(abi=self._abi, bytecode=self._bytecode)
        nonce = w3.eth.getTransactionCount(self._ADDRESS)
        # set up transaction from constructor which executes when firstly
        transaction = Trader.constructor(router, token0, token1, fee).buildTransaction(
            {"chainId": self._CHAINID, "from": self._ADDRESS, "nonce": nonce}
        )

        signed_tx = self.sign(w3, transaction)

        tx_receipt = self.send(w3, signed_tx)

        return tx_receipt
