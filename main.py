from execution import Executor

from deployment import Deployer


class Main:

    def __init__(self, RPC_URL, CHAINID, ADDRESS):
        self.rpc_url = RPC_URL
        self.account_address = ADDRESS
        self.chain_id = CHAINID

    def main(self):

        deployer = Deployer(self.rpc_url, self.chain_id,
                            self.account_address, 'Trader')

        deployer.deploy_Trader()
