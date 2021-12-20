from flask.scaffold import F
import pandas as pd
import sqlalchemy
import tqdm
from typing import Tuple

from block import Block
from document import Document
from similarity import Similarity

class Blockchain:
    def __init__(self, load_database: bool=False):
        """
        Classe representando um Blockchain.

        Args
            load_database (bool): Determina se o Blockchain deve ser criado do começo (utilizando um bloco
            de gênesis) ou se deve ser inicializado a partir de um banco de dados.
        """
        self._chain = []
        self._incoming_data = None
        if load_database:
            self._load_database()
        else:
            self._create_genesis_block()
        
    def save_database(self):
        print("Saving database...")
        columns_names = list(self.last_block.info.keys())[2:] + ["First_title", "First_body", "Second_title", "Second_body", "Similarity"]
        chain_data = []
        for block in tqdm.tqdm(self._chain):
            # Recupera os dados contidos em um bloco (índice, data, hash etc.)
            block_info = [str(data) for data in block.info.values()]

            # Recupera os dados contidos no bloco para serem salvos com todos os campos (nome dos arquivos, corpo dos documentos e similaridade)
            transaction = block.info["Transaction"]
            first_document, second_document = transaction.documents
            block_info.extend([first_document.title, first_document.body, second_document.title, second_document.body, transaction.similarity])
            chain_data.append(block_info[2:])
        dataframe = pd.DataFrame(chain_data, columns=columns_names)
        
        sql_engine = sqlalchemy.create_engine("sqlite:///blockchain.db", echo=False)
        dataframe.to_sql("Blockchain", con=sql_engine, if_exists="replace")

        print("Save database complete!")

    def _load_database(self):
        print(f"Loading Database...")
        sql_engine = sqlalchemy.create_engine("sqlite:///blockchain.db", echo=False)
        dataframe = pd.read_sql("Blockchain", con=sql_engine)

        for _, row in tqdm.tqdm(dataframe.iterrows(), total=dataframe.shape[0]):
            row = list(row)
            first_document, second_document = Document(row[-5], row[-4]), Document(row[-3], row[-2])
            similarity = Similarity(first_document, second_document, row[-1])
            block = Block(index=row[0], data=similarity, previous_hash=row[2], hash=row[3], nounce=row[4])
            self._chain.append(block)
        print("Load database complete!")

    def _create_genesis_block(self):
        """
        Cria um bloco primordial para o Blockchain.
        """
        blockchain_doc, ai_doc = Document("Satoshi-Nakamoto", "Blockchain will change the world!"), Document("Andrew-Ng", "AI will change the world!")
        genesis_block = Block(0, Similarity(blockchain_doc, ai_doc), "0"*32)
        self._chain.append(genesis_block)

    @property
    def last_block(self):
        """
        Retorna uma referência para o último bloco inserido no Blockchain.
        """
        return self._chain[-1]
    
    def add_transaction(self, first_document: Document, second_document: Document):
        """
        Registra os dados (documentos a serem comparados) de uma nova transação.

        Args:
            first_string, second_string (Document): documents em que se 
            deve aplicar o cálculo de similaridade semântica.
        """
        self._incoming_data = (first_document, second_document)

    def mine(self):
        if self._incoming_data is None:
            return None

        found, text_similarity = self._search_texts()
        if found:
            print(f"Similaridade entre os documentos {' e '.join([doc.title for doc in self._incoming_data])} já havia sido calculada anteriormente.")
            return text_similarity

        last_block = self.last_block
        previous_hash = last_block.hash
        self._chain.append(Block(last_block.index + 1, Similarity(*self._incoming_data), previous_hash))
        self._incoming_data = None
        
        # Nesse ponto, um novo bloco foi inserido de forma bem sucedida, e retorna-se a similaridade calculada
        # entre os textos fornecidos. Também pode-se atualizar o banco de dados.
        self.save_database()
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
            if block.data.same_document(self._incoming_data):
                return (True, block.data.similarity)
        
        return (False, 0.0)

    def __str__(self) -> str:
        chain_info = ""
        for block in self._chain:
            block_info_descriptions = ("Transaction", "Timestamp", "Previous-Hash", "Hash", "Nounce")
            block_info = list(block.info.values())[1:]
            block_text = f"Block {block.index}\n" 
            block_text += '\n'.join([f"\t{description}: {info}" for description, info in zip(block_info_descriptions, block_info)])
            chain_info += f"{block_text}\n"
        
        return chain_info

if __name__ == "__main__":
    blockchain = Blockchain()
    sample_data = [
        (Document("king", "long live the king"), Document("queen", "long live the queen")),
        (Document("Apple", "history of a company"), Document("Fruit", "history of an apple")),
        (Document("sun", "light"), Document("moon", "dark")),
        (Document("love", "heart"), Document("heart", "love")),
        (Document("king", "long live the king"), Document("queen", "long live the queen")),
        (Document("moon", "dark"), Document("sun", "light")),
    ]
    
    for idx, texts in enumerate(sample_data):
        blockchain.add_transaction(*texts)
        blockchain.mine()    
    
    print(blockchain)
    blockchain.save_database()
    
    new_blockchain = Blockchain(load_database=True)
    print(f"Creating a new blockchain from the previous one...")
    print(new_blockchain)