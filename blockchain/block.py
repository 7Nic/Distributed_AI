from datetime import datetime
from typing import Any

from validation import to_hash, is_valid_proof

class Block:
    def __init__(self, index: int, data: Any, previous_hash, proof: int):
        """
        Classe definindo um bloco de um Blockchain.

        Args:
            index (int): índice do bloco no Blockchain
            data (Any): dados a serem armazenados no bloco.
            previous_hash: hash do bloco anterior.
            proof (int): valor único utilizado para o Proof of Work dos blocos.
        """        
        self._index = index
        self._data = data
        self._timestamp = datetime.utcnow()
        self._previous_hash = previous_hash
        self._nounce = 0
        self._hash = self.proof_of_work()
    
    def proof_of_work(self):
        current_hash = to_hash(str(self))
        while not is_valid_proof(current_hash):
            self._nounce += 1
            current_hash = to_hash(str(self))
        return current_hash

    @property
    def hash(self):
        return self._hash

    def __str__(self):
        return f"{self._index} {self._data} {self._timestamp} {self._previous_hash} {self._nounce}"