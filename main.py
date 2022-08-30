from deployment import Deployer
import os

from dotenv import load_dotenv


class Main:

    def __init__(self, RPC_URL, CHAINID, ADDRESS):
        self.rpc_url = RPC_URL
        self.account_address = ADDRESS
        self.chain_id = CHAINID

    def main(self, router, token0, token1, fee):

        deployer = Deployer(self.rpc_url, self.chain_id,
                            self.account_address, 'Trader')

        tx = deployer.deploy_Trader(router, token0, token1, fee)

        return tx


if __name__ == "__main__":

    load_dotenv()
    private_key = os.environ.get('PRIVATE_KEY')
    address = os.environ.get('ADDRESS')
    chainid = os.environ.get('CHAIN_ID')
    rpc_url = os.environ.get('ROPSTEN_URL')

    UNIV3_ropsten_router = '0xE592427A0AEce92De3Edee1F18E0157C05861564'

    WETH_ropsten = '0xc778417E063141139Fce010982780140Aa0cD5Ab'

    DAI_ropsten = '0x31F42841c2db5173425b5223809CF3A38FEde360'

    # fee 3000 = 0.3%
    fee = 3000

    main = Main(rpc_url, chainid, address)

    main.main(UNIV3_ropsten_router, WETH_ropsten, DAI_ropsten, fee)
