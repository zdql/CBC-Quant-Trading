from web3 import Web3
from dotenv import load_dotenv
from constants import UNISWAPV3_POOL_ABI
import os
import json


load_dotenv()


class Executor():

    def __init__(self, RPC_URL, Oracle_Pool, Trader, TraderAbi, CHAINID, ADDRESS):

        self._url = RPC_URL
        self._pool = Oracle_Pool
        self.pool_abi = UNISWAPV3_POOL_ABI
        self._Trader = Trader
        self._TraderAbi = TraderAbi
        self._CHAINID = CHAINID
        self._ADDRESS = ADDRESS
        self._PRIVATE_KEY = os.getenv('PRIVATE_KEY')

    def get_prices(self):

        provider = Web3(Web3.WebsocketProvider(self._url))
        pool_contract = provider.eth.contract(
            self._pool, abi=self.pool_abi)

        response = pool_contract.functions.slot0().call()

        price_token0 = ((response[0] ** 2) / (2 ** 192)) * 100

        price_token1 = ((2 ** 192) / (response[0] ** 2)) * 100

        return price_token0, price_token1

    def call_Trader(self):

        provider = Web3(Web3.WebsocketProvider(self._url))
        pool_contract = provider.eth.contract(
            address=self._Trader, abi=self._TraderAbi)

        call_fun = pool_contract.functions.store(5).buildTransaction(
            {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
        )
        sign_call_fun = w3.eth.account.signTransaction(
            call_fun, private_key=private_key)
        tx_call_fun_hash = w3.eth.send_raw_transaction(
            sign_call_fun.rawTransaction)
        tx_call_fun_receipt = w3.eth.wait_for_transaction_receipt(
            tx_call_fun_hash)

        print(storage_sol.functions.retrieve().call())


if __name__ == '__main__':
    RPCURL = os.environ.get('POLYGON_URL')
    WBTCUSDC = '0x847b64f9d3A95e977D157866447a5C0A5dFa0Ee5'

    E = Executor(RPCURL, WBTCUSDC)
    print(E.get_prices())

    ROPSTENURL = os.environ.get('ROPSTEN_URL')
