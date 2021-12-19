from datetime import datetime
from typing import Any

from validation import to_hash

class Block:
    def __init__(self, data: Any, previous_hash, proof: int):
        """
        Classe definindo um bloco de um Blockchain.

        Args:
            data (Any): dados a serem armazenados no bloco.
            previous_hash: hash do bloco anterior.
            proof (int): valor único utilizado para o Proof of Work dos blocos.
        """        
        self._data = data
        self._timestamp = datetime.utcnow()
        self._previous_hash = previous_hash
        self._proof = proof
        self._hash = to_hash(str(self))
    
    def __str__(self):
        return f"{self._data} {self._timestamp} {self._previous_hash} {self._proof}"