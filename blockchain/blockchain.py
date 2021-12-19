from block import Block

class Blockchain:
    """
    Classe representando um Blockchain.
    """
    def __init__(self):
        self._chain = []
        self._create_genesis_block()
        self._incoming_data = None
    
    def _create_genesis_block(self):
        self._chain.append(Block(0, None, "0"*32))

    @property
    def last_block(self):
        return self._chain[-1]
    
    def add_transaction(self, str1, str2):
        similarity = 0.7 # PLACEHOLDER
        self._incoming_data = (str1, str2, similarity)

    def mine(self):
        if self._incoming_data is None:
            return

        last_block = self.last_block
        previous_hash = last_block.hash
        self._chain.append(Block(last_block.index + 1, self._incoming_data, previous_hash=previous_hash))
        self._incoming_data = None
    
    def print(self):
        """
        DEBUG
        """
        for idx, block in enumerate(self._chain):
            print(f"Block {idx}: {block}")