from .transaction import Transaction
from ..vocabulary import Vocabulary


class Buy(Transaction):
    def __init__(self):
        super().__init__()
        self.strategies = []

    """
    TODO: Define the expected vocabulary
    """

    def when(self, cmd):
        instructions = Vocabulary.parse_cmd(cmd)
