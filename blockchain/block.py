from datetime import datetime
from typing import Any

from validation import to_hash, is_valid_proof

class Block:
    def __init__(self, index: int, data: Any, previous_hash):
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
        """
        Calcula o nounce (number only computed once), que é um número adicionado ao
        hash do bloco criado para atender às restrições de dificuldade criptográficas.
        Como consequência, recalcula também o hash do bloco criado.

        Returns:
            current_hash: novo hash calculado para o bloco, baseado no nounce determinado.
        """
        current_hash = to_hash(str(self))
        while not is_valid_proof(current_hash):
            self._nounce += 1
            current_hash = to_hash(str(self))
        return current_hash

    @property
    def info(self):
        return {
            "index": self._index, 
            "data": self._data, 
            "timestamp": self._timestamp, 
            "previous_hash": self._previous_hash, 
            "nounce": self._nounce
        }
    
    @property
    def data(self):
        return self._data

    @property
    def hash(self):
        return self._hash
    
    @property
    def index(self):
        return self._index

    def __str__(self):
        return f"{self._index} {self._data} {self._timestamp} {self._previous_hash} {self._nounce}"