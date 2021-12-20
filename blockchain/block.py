from datetime import datetime
from typing import Any

from validation import to_hash, is_valid_proof

class Block:
    def __init__(self, index: int, data: Any, previous_hash, timestamp=None, nounce: int=None, hash=None):
        """
        Classe definindo um bloco de um Blockchain.

        Args:
            index (int): índice do bloco no Blockchain
            previous_hash: hash do bloco anterior.
            data (Any): dados a serem armazenados no bloco.
            timestamp (datetime): Tempo em que o bloco foi criado. Por padrão é None; neste caso, o
            o valor será aquele retornado no momento da criação da instância.
            nounce (int): número utilizado na criptografia do bloco. Por padrão é None; neste caso,
            o valor será calculado através do mecanismo de Proof of Work.
            hash: hash do bloco. Por padrão é None; neste caso, o hash será calculado a partir do
            mecanismo de Proof of Work, utilizando os demais atributos do bloco (incluindo o nounce).
        """        
        self._index = index
        self._data = data
        self._previous_hash = previous_hash
        self._timestamp = timestamp if timestamp is not None else datetime.utcnow()
        self._nounce = nounce if nounce is not None else 0
        self._hash = hash if hash is not None else self.proof_of_work()
    
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
            "Index": self._index, 
            "Transaction": self._data, 
            "Timestamp": self._timestamp, 
            "Previous_hash": self._previous_hash,
            "Hash": self._hash,
            "Nounce": self._nounce
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