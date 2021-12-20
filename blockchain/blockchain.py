from os import path
import pathlib
from typing import Tuple

from block import Block
from similarity import Similarity

class Blockchain:
    def __init__(self, database_path: pathlib.Path=None, load: bool=False):
        """
        Classe representando um Blockchain.
        """
        self._chain = []
        self._incoming_data = None
        if load:
            self._load_database()
        else:
            self._create_genesis_block()
        
    def save_database(self):
        pass

    def _load_database(self):
        pass

    def _create_genesis_block(self):
        """
        Cria um bloco primordial para o Blockchain.
        """
        genesis_block = Block(0, Similarity("Satoshi", "Nakamoto"), "0"*32)
        self._chain.append(genesis_block)

    @property
    def last_block(self):
        """
        Retorna uma referência para o último bloco inserido no Blockchain.
        """
        return self._chain[-1]
    
    def add_transaction(self, first_string: str, second_string: str):
        """
        Registra os dados (textos a serem comparados) de uma nova transação.

        Args:
            first_string, second_string (str): textos em que se 
            deve aplicar o cálculo de similaridade semântica.
        """
        self._incoming_data = (first_string, second_string)

    def mine(self):
        if self._incoming_data is None:
            return None

        found, text_similarity = self._search_texts()
        if found:
            print(f"Similaridade entre os textos {' e '.join([*self._incoming_data])} já havia sido calculada anteriormente.")
            return text_similarity

        last_block = self.last_block
        previous_hash = last_block.hash
        self._chain.append(Block(last_block.index + 1, Similarity(*self._incoming_data), previous_hash))
        self._incoming_data = None
        
        # Nesse ponto, um novo bloco foi inserido de forma bem sucedida, e retorna-se a similaridade calculada
        # entre os textos fornecidos.
        return self.last_block.data.similarity
    
    def _search_texts(self) -> Tuple[bool, float]:
        """
        Verifica se a transação pendente (contendo textos a serem comparados)
        já foi inserida previamente no Blockchain. Caso já tenha sido inserida,
        pode-se retornar a similaridade previamente calculada sem gastar recursos
        computacionais na inferência do modelo de rede neural (evitando-se recalcular
        desnecessariamente a similaridade entre textos), e também sem gastar recursos
        computacionais inserindo um bloco redundante do modelo (evitando-se gastar tempo
        na operação de Proof of Work).

        Retunrs
            Tuple[bool, float]: Caso a transação pendente já tenha sido inserida previamente
            no Blockchain, retorna-se uma tupla contendo True e o valor da similaridade calculada
            anteriormente. Caso a transação pendente não tenha sido inserida no Blockchain antes,
            retorna uma tupla contendo False e 0.0
        """
        for block in self._chain:
            if block.data.same_text(self._incoming_data):
                return (True, block.data.similarity)
        
        return (False, 0.0)

    def __str__(self) -> str:
        chain_info = ""
        for block in self._chain:
            block_info_descriptions = ("Transaction", "Timestamp", "Previous-Hash", "Nounce")
            block_info = list(block.info.values())[1:]
            block_text = f"Block {block.index}\n" 
            block_text += '\n'.join([f"\t{description}: {info}" for description, info in zip(block_info_descriptions, block_info)])
            chain_info += f"{block_text}\n"
        
        return chain_info

if __name__ == "__main__":
    blockchain = Blockchain()
    sample_data = [
        ("king", "queen"),
        ("apple", "fruit"),
        ("sun", "light"),
        ("love", "heart")
    ]
    
    for idx, texts in enumerate(sample_data):
        blockchain.add_transaction(*texts)
        blockchain.mine()    
    
    print(blockchain)